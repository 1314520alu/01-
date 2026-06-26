#!/usr/bin/env python3
"""为 Core 载板原理图 U1/U2 连接器批量添加引脚网络（经 JLCEDA MCP HTTP）。

每个信号 Pin：
  1. 从引脚沿竖直方向拉导线，并用 Wire.create(line, net) 赋网络名（嘉立创可见）
  2. createNetLabel 在当前 MCP 下不生效，已弃用
  - rotation=90：向下 (y + stub)
  - rotation=270：向上 (y - stub)
  - stub 同排 **统一长度**：按该排最长网络名 × CHAR_PITCH × scale + MARGIN
  - 默认包含 GND；NC 默认跳过（用 assign_nc_no_connect.py 删线并挂 No Connect）
  - 若仍需 NC 短线标 net 名：加 --wire-nc

用法：
  python3 tools/assign_core_carrier_nets.py --replace --designator U1
  python3 tools/assign_core_carrier_nets.py --replace --safe-stub   # 仅 8mil 短线
  python3 tools/assign_nc_no_connect.py                             # NC 引脚 No Connect
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "DF17" / "schematic" / "core-carrier-schematic-spec.json"
MCP_URL = "http://127.0.0.1:7655/mcp"

PART_NUMBERS = {
    "DF17(1.0H)-80DP-0.5V(57)",
    "DF17(3.0)-80DS-0.5V(57)",
    "DF17(3.0H)-80DS-0.5V(57)",
}

NET_SOURCE_PART = {
    "DF17(1.0H)-80DP-0.5V(57)": "DF17(1.0H)-80DP-0.5V(57)",
    "DF17(3.0)-80DS-0.5V(57)": "DF17(3.0)-80DS-0.5V(57)",
    "DF17(3.0H)-80DS-0.5V(57)": "DF17(3.0)-80DS-0.5V(57)",
}

SIGNAL_PIN_MAX = 80
CHAR_PITCH = 12
MARGIN = 20
MIN_STUB = 40
SAFE_STUB = 8
STUB_SCALE = 1 / 3  # 导线长度 = 适应最长网络名 × 此比例（当前 1/3）
COORD_TOL = 1.0
REGION_PAD = 30
REGION_PAD_STUB = 320

TOP_ROTATION = 90
BOTTOM_ROTATION = 270


def mcp_call(tool: str, arguments: dict, req_id: int = 1) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.load(resp)
    if "error" in body:
        raise RuntimeError(body["error"].get("message", str(body["error"])))
    return body["result"]


def api_invoke(api_full_name: str, args: list, req_id: int, timeout_ms: int = 120_000):
    result = mcp_call(
        "api_invoke",
        {"apiFullName": api_full_name, "args": args, "timeoutMs": timeout_ms},
        req_id,
    )
    text = result["content"][0]["text"]
    data = json.loads(text)
    if "error" in data:
        raise RuntimeError(f"{api_full_name}: {data['error']}")
    return data.get("result", data)


def coords_near(ax: float, ay: float, bx: float, by: float, tol: float = COORD_TOL) -> bool:
    return abs(ax - bx) <= tol and abs(ay - by) <= tol


def stub_for_net(
    net: str,
    char_pitch: int,
    margin: int,
    long_stub: bool,
    stub_scale: float,
) -> int:
    if not long_stub:
        return SAFE_STUB
    full = max(MIN_STUB, len(net) * char_pitch + margin)
    return max(SAFE_STUB, int(full * stub_scale))


def max_stub_for_rotation(
    pin_nets: dict[str, str],
    pin_by_num: dict[str, dict],
    rotation: int,
    char_pitch: int,
    margin: int,
    override: int | None,
    long_stub: bool,
    stub_scale: float,
    *,
    wire_gnd: bool,
    wire_nc: bool,
) -> int:
    if override is not None:
        return override
    stubs: list[int] = []
    for pin_num, net in pin_nets.items():
        if not net:
            continue
        if net == "NC" and not wire_nc:
            continue
        if net == "GND" and not wire_gnd:
            continue
        pin = pin_by_num.get(pin_num)
        if not pin or pin.get("rotation") != rotation:
            continue
        stubs.append(stub_for_net(net, char_pitch, margin, long_stub, stub_scale))
    if not stubs:
        return SAFE_STUB if not long_stub else max(SAFE_STUB, int(MIN_STUB * stub_scale))
    return max(stubs)


def wire_line_pin_direction(
    x: float,
    y: float,
    rotation: int,
    stub: int,
    flip: bool = False,
) -> list[float]:
    """沿引脚朝外竖直直线：rotation=90 向下，rotation=270 向上。"""
    if rotation == TOP_ROTATION:
        dy = stub if not flip else -stub
        return [x, y, x, y + dy]
    if rotation == BOTTOM_ROTATION:
        dy = -stub if not flip else stub
        return [x, y, x, y + dy]
    if rotation == 0:
        return [x, y, x + stub, y]
    if rotation == 180:
        return [x, y, x - stub, y]
    dy = -stub if not flip else stub
    return [x, y, x, y + dy]


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


PART_ALIASES: dict[str, str] = {
    "DF17(3.0H)-80DS-0.5V(57)": "DF17(3.0)-80DS-0.5V(57)",
}


def canonical_part(part: str) -> str:
    return PART_ALIASES.get(part, part)


def part_from_component(comp: dict) -> str | None:
    for key in ("schematicSubPartName", "componentSymbolName", "componentValue", "componentName"):
        value = comp.get(key) or ""
        for part in PART_NUMBERS:
            if part in value:
                return canonical_part(part)
    return None


def build_net_maps(spec: dict, components: list[dict]) -> dict[str, dict[str, str]]:
    part_to_pins: dict[str, dict[str, str]] = {}
    for conn in spec["connectors"]:
        part = conn["part_number"]
        source = NET_SOURCE_PART.get(part, part)
        if source in part_to_pins:
            continue
        src_conn = next((c for c in spec["connectors"] if c["part_number"] == source), conn)
        part_to_pins[source] = {
            str(p["pin"]): p["net"] for p in src_conn["pins"] if p["pin"] <= SIGNAL_PIN_MAX
        }
    for part, pin_map in list(part_to_pins.items()):
        part_to_pins[canonical_part(part)] = pin_map

    maps: dict[str, dict[str, str]] = {}
    for comp in components:
        part = part_from_component(comp)
        designator = comp.get("componentDesignator")
        if not part or not designator:
            continue
        pin_map = part_to_pins.get(part) or part_to_pins.get(canonical_part(part))
        if not pin_map:
            continue
        maps[designator] = pin_map
        kind = "DS" if "80DS" in part else "DP"
        pin1 = pin_map.get("1", "")
        if kind == "DS" and pin1 in ("SCK_EXT1", "CAN2_N", "MISO_EXT1"):
            print(
                f"WARN {designator}: DS 座子 Pin1={pin1} 像 Core DS 表，载板 DS 应标 Core DP 网络",
                file=sys.stderr,
            )
        if kind == "DP" and pin1 in ("CTS_TELEM3", "VBUS", "RX_TELEM3"):
            print(
                f"WARN {designator}: DP 座子 Pin1={pin1} 像 Core DP 表，载板 DP 应标 Core DS 网络",
                file=sys.stderr,
            )
    return maps


def read_schematic_components(req_id: int) -> list[dict]:
    result = mcp_call("schematic_read", {}, req_id)
    snap = json.loads(json.loads(result["content"][0]["text"])["schematicCircuitSnapshot"])
    return snap["components"]


def pin_bbox(
    pins: list[dict],
    stub_top: int,
    stub_bottom: int,
    *,
    tight: bool = False,
) -> tuple[int, int, int, int]:
    signal = [p for p in pins if p["pinNumber"].isdigit() and int(p["pinNumber"]) <= SIGNAL_PIN_MAX]
    xs = [p["x"] for p in signal]
    ys = [p["y"] for p in signal]
    pad = max(stub_top, stub_bottom) + REGION_PAD if tight else max(stub_top, stub_bottom, REGION_PAD_STUB)
    return (
        int(min(xs) - REGION_PAD - pad),
        int(max(xs) + REGION_PAD + pad),
        int(min(ys) - REGION_PAD - pad),
        int(max(ys) + REGION_PAD + pad),
    )


def wire_in_bbox(wire: dict, left: int, right: int, top: int, bottom: int) -> bool:
    line = wire.get("line") or []
    if not line:
        return False
    segments = line if isinstance(line[0], list) else [line]
    for seg in segments:
        if len(seg) < 4:
            continue
        xs = seg[0::2]
        ys = seg[1::2]
        if max(xs) >= left and min(xs) <= right and max(ys) >= top and min(ys) <= bottom:
            return True
    return False


def normalize_line(line: list) -> list[float]:
    if line and isinstance(line[0], list):
        return list(line[0])
    return list(line)


def wire_length(line: list[float]) -> float:
    x1, y1, x2, y2 = line[:4]
    return abs(x2 - x1) if abs(y2 - y1) < abs(x2 - x1) else abs(y2 - y1)


def wire_at_pin(wires: list[dict], pin: dict) -> dict | None:
    px, py = pin["x"], pin["y"]
    for wire in wires:
        line = normalize_line(wire.get("line") or [])
        if len(line) < 4:
            continue
        if coords_near(line[0], line[1], px, py) or coords_near(line[2], line[3], px, py):
            return wire
    return None


def delete_all_wires(req_id: int) -> int:
    deleted = 0
    while True:
        wires = api_invoke("eda.sch_PrimitiveWire.getAll", [], req_id)
        req_id += 1
        if not isinstance(wires, list) or not wires:
            break
        ids = [w["primitiveId"] for w in wires]
        for start in range(0, len(ids), 50):
            batch = ids[start : start + 50]
            if batch:
                api_invoke("eda.sch_PrimitiveWire.delete", [batch], req_id)
                req_id += 1
                deleted += len(batch)
        if len(wires) < 120:
            break
    print(f"purged {deleted} wires total")
    return req_id


def delete_wires_near_component(
    pins: list[dict],
    req_id: int,
    dry_run: bool,
    stub_top: int,
    stub_bottom: int,
) -> tuple[int, int]:
    left, right, top, bottom = pin_bbox(pins, stub_top, stub_bottom, tight=True)
    wires = api_invoke("eda.sch_PrimitiveWire.getAll", [], req_id)
    req_id += 1
    if not isinstance(wires, list):
        wires = []
    to_delete = [w["primitiveId"] for w in wires if wire_in_bbox(w, left, right, top, bottom)]
    if dry_run:
        print(f"  would delete {len(to_delete)} wires in bbox ({left},{top})-({right},{bottom})")
        return req_id, len(to_delete)
    for start in range(0, len(to_delete), 50):
        batch = to_delete[start : start + 50]
        if batch:
            api_invoke("eda.sch_PrimitiveWire.delete", [batch], req_id)
            req_id += 1
    return req_id, len(to_delete)


def assign_nets(
    dry_run: bool = False,
    only: str | None = None,
    replace: bool = False,
    char_pitch: int = CHAR_PITCH,
    margin: int = MARGIN,
    stub_top: int | None = None,
    stub_bottom: int | None = None,
    flip: bool = False,
    long_stub: bool = True,
    purge_all_wires: bool = False,
    stub_scale: float = STUB_SCALE,
    wire_gnd: bool = True,
    wire_nc: bool = False,
) -> None:
    spec = load_spec()
    components = read_schematic_components(10)
    net_maps = build_net_maps(spec, components)
    by_designator = {c["componentDesignator"]: c for c in components}
    req_id = 100

    if purge_all_wires and not dry_run:
        req_id = delete_all_wires(req_id)
        print("purged all wires on page")

    for designator, pin_nets in sorted(net_maps.items()):
        if only and designator != only:
            continue
        comp = by_designator.get(designator)
        if not comp:
            print(f"SKIP {designator}: 原理图中未找到该位号", file=sys.stderr)
            continue

        primitive_id = comp["componentInstanceId"]
        pins = api_invoke(
            "eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId",
            [primitive_id],
            req_id,
        )
        req_id += 1

        pin_by_num = {
            p["pinNumber"]: p
            for p in pins
            if p["pinNumber"].isdigit() and int(p["pinNumber"]) <= SIGNAL_PIN_MAX
        }

        stub_top_len = max_stub_for_rotation(
            pin_nets,
            pin_by_num,
            TOP_ROTATION,
            char_pitch,
            margin,
            stub_top,
            long_stub,
            stub_scale,
            wire_gnd=wire_gnd,
            wire_nc=wire_nc,
        )
        stub_bottom_len = max_stub_for_rotation(
            pin_nets,
            pin_by_num,
            BOTTOM_ROTATION,
            char_pitch,
            margin,
            stub_bottom,
            long_stub,
            stub_scale,
            wire_gnd=wire_gnd,
            wire_nc=wire_nc,
        )
        mode = "uniform stub" if long_stub else f"safe-stub={SAFE_STUB}"
        print(
            f"{designator}: max stub top={stub_top_len} bottom={stub_bottom_len} mil "
            f"[{mode} scale={stub_scale}]"
        )

        if replace and not purge_all_wires:
            req_id, deleted = delete_wires_near_component(
                pins, req_id, dry_run, stub_top_len, stub_bottom_len
            )
            print(f"{designator}: deleted {deleted} old wires in bbox")

        wires_cache = api_invoke("eda.sch_PrimitiveWire.getAll", [], req_id)
        req_id += 1
        if not isinstance(wires_cache, list):
            wires_cache = []

        ok, skip, fail, replaced, kept = 0, 0, 0, 0, 0

        for pin_num in sorted(pin_by_num, key=int):
            net = pin_nets.get(pin_num)
            if not net:
                skip += 1
                continue
            if net == "NC" and not wire_nc:
                skip += 1
                continue
            if net == "GND" and not wire_gnd:
                skip += 1
                continue

            pin = pin_by_num[pin_num]
            rot = pin.get("rotation", TOP_ROTATION)
            if rot == TOP_ROTATION:
                stub = stub_top_len
            elif rot == BOTTOM_ROTATION:
                stub = stub_bottom_len
            else:
                stub = max(stub_top_len, stub_bottom_len)

            px, py = pin["x"], pin["y"]
            line = wire_line_pin_direction(px, py, rot, stub, flip)

            if dry_run:
                if pin_num in ("1", "2", "79", "80"):
                    print(
                        f"  {designator}.{pin_num} -> {net}  label@({px},{py})  "
                        f"wire {line} stub={stub}"
                    )
                ok += 1
                continue

            existing = wire_at_pin(wires_cache, pin)
            if existing:
                old_len = wire_length(normalize_line(existing.get("line") or []))
                if abs(old_len - stub) <= COORD_TOL and existing.get("net") == net:
                    kept += 1
                    ok += 1
                    continue
                api_invoke("eda.sch_PrimitiveWire.delete", [[existing["primitiveId"]]], req_id)
                req_id += 1
                wires_cache = [
                    w for w in wires_cache if w["primitiveId"] != existing["primitiveId"]
                ]
                replaced += 1

            try:
                created = api_invoke("eda.sch_PrimitiveWire.create", [line, net], req_id)
                req_id += 1
                wires_cache.append(created)
                ok += 1
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL {designator}.{pin_num} ({net}): {exc}", file=sys.stderr)
                fail += 1

        print(
            f"{designator}: assigned {ok}, kept {kept}, replaced {replaced}, "
            f"skipped {skip}, failed {fail}"
        )

    if not dry_run:
        saved = api_invoke("eda.sch_Document.save", [], req_id)
        print(f"save: {saved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assign DF17 carrier nets via JLCEDA MCP")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--purge-all-wires", action="store_true", help="Delete every wire on page before assign")
    parser.add_argument("--designator", help="Only U1 or U2")
    parser.add_argument("--char-pitch", type=int, default=CHAR_PITCH)
    parser.add_argument("--margin", type=int, default=MARGIN)
    parser.add_argument("--stub-top", type=int, default=None)
    parser.add_argument("--stub-bottom", type=int, default=None)
    parser.add_argument("--stub-scale", type=float, default=STUB_SCALE, help="Stub length multiplier (default 1/3)")
    parser.add_argument("--flip", action="store_true", help="Reverse fanout direction")
    parser.add_argument(
        "--safe-stub",
        action="store_true",
        help="Use 8 mil stub only (default: uniform stub from longest net name)",
    )
    parser.add_argument(
        "--skip-gnd",
        action="store_true",
        help="Skip GND pins (default: wire and label GND)",
    )
    parser.add_argument(
        "--wire-nc",
        action="store_true",
        help="Wire NC pins with net name NC (default: skip; use assign_nc_no_connect.py)",
    )
    args = parser.parse_args()

    try:
        assign_nets(
            dry_run=args.dry_run,
            only=args.designator,
            replace=args.replace,
            char_pitch=args.char_pitch,
            margin=args.margin,
            stub_top=args.stub_top,
            stub_bottom=args.stub_bottom,
            flip=args.flip,
            long_stub=not args.safe_stub,
            purge_all_wires=args.purge_all_wires,
            stub_scale=args.stub_scale,
            wire_gnd=not args.skip_gnd,
            wire_nc=args.wire_nc,
        )
    except urllib.error.URLError as exc:
        print("无法连接 JLCEDA MCP (http://127.0.0.1:7655)。", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
