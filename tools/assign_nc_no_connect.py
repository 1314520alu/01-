#!/usr/bin/env python3
"""为 Core 载板 DF17 连接器 NC 引脚删除 NC 导线并设置 No Connect（嘉立创 MCP）。

流程（与手动操作一致）：
  1. 删除 NC 引脚上的导线（去掉 ``NC`` 网络名，避免多脚被同名网络连在一起）
  2. 调用 ``eda.sch_PrimitivePin.modify(..., {noConnected: true})`` 设置非连接标识（×）

说明：Bridge 当前 ``sch_PrimitivePin.modify`` 的 property 未文档化 ``noConnected`` 字段，
脚本会尝试写入并在保存前校验；若仍为 false，请在 EDA 内对列出的 Pin 手动挂 No Connect。

用法：
  python3 tools/assign_nc_no_connect.py --dry-run
  python3 tools/assign_nc_no_connect.py
  python3 tools/assign_nc_no_connect.py --designator U1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from assign_core_carrier_nets import (
    SIGNAL_PIN_MAX,
    api_invoke,
    build_net_maps,
    load_spec,
    read_schematic_components,
    wire_at_pin,
)


def set_pin_no_connected(pin_id: str, req_id: int, dry_run: bool) -> bool:
    if dry_run:
        return True
    try:
        api_invoke(
            "eda.sch_PrimitivePin.modify",
            [pin_id, {"noConnected": True}],
            req_id,
        )
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  WARN modify noConnected failed for {pin_id}: {exc}", file=sys.stderr)
        return False


def verify_no_connected(component_id: str, pin_num: str, req_id: int) -> bool | None:
    pins = api_invoke(
        "eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId",
        [component_id],
        req_id,
    )
    req_id += 1
    for pin in pins:
        if pin.get("pinNumber") == pin_num:
            return bool(pin.get("noConnected"))
    return None


def assign_nc_no_connect(
    dry_run: bool = False,
    only: str | None = None,
) -> None:
    spec = load_spec()
    components = read_schematic_components(10)
    net_maps = build_net_maps(spec, components)
    by_designator = {c["componentDesignator"]: c for c in components}
    req_id = 200

    wires_cache = api_invoke("eda.sch_PrimitiveWire.getAll", [], req_id)
    req_id += 1
    if not isinstance(wires_cache, list):
        wires_cache = []

    deleted_wires = 0
    nc_pins: list[tuple[str, str, str]] = []
    set_ok = 0
    set_fail = 0
    verify_ok = 0
    verify_fail = 0
    need_manual: list[str] = []

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

        for pin_num in sorted(
            (n for n, net in pin_nets.items() if net == "NC"),
            key=int,
        ):
            pin = pin_by_num.get(pin_num)
            if not pin:
                print(f"WARN {designator}.{pin_num}: 未找到引脚", file=sys.stderr)
                continue

            nc_pins.append((designator, pin_num, pin["primitiveId"]))
            wire = wire_at_pin(wires_cache, pin)
            if wire:
                if wire.get("net") != "NC":
                    print(
                        f"WARN {designator}.{pin_num}: 导线网络为 {wire.get('net')!r}，非 NC，跳过删线",
                        file=sys.stderr,
                    )
                elif dry_run:
                    deleted_wires += 1
                    print(f"  would delete wire on {designator}.{pin_num} ({wire['primitiveId']})")
                else:
                    api_invoke(
                        "eda.sch_PrimitiveWire.delete",
                        [[wire["primitiveId"]]],
                        req_id,
                    )
                    req_id += 1
                    wires_cache = [
                        w for w in wires_cache if w["primitiveId"] != wire["primitiveId"]
                    ]
                    deleted_wires += 1

            if set_pin_no_connected(pin["primitiveId"], req_id, dry_run):
                set_ok += 1
            else:
                set_fail += 1

    if not dry_run and nc_pins:
        for designator, pin_num, _pin_id in nc_pins:
            comp = by_designator[designator]
            state = verify_no_connected(comp["componentInstanceId"], pin_num, req_id)
            req_id += 1
            label = f"{designator}.{pin_num}"
            if state is True:
                verify_ok += 1
            else:
                verify_fail += 1
                need_manual.append(label)
                print(f"VERIFY FAIL {label}: noConnected={state!r} — 请在 EDA 手动挂 No Connect（×）")

    print(
        f"NC pins: {len(nc_pins)}, wires removed: {deleted_wires}, "
        f"modify attempted: {set_ok}, modify failed: {set_fail}, "
        f"verified noConnected: {verify_ok}, need manual: {verify_fail}"
    )
    if need_manual:
        print("Manual No Connect required for:", ", ".join(need_manual))

    nc_left = [w for w in wires_cache if w.get("net") == "NC"]
    if nc_left:
        print(f"cleanup: {len(nc_left)} remaining NC net wire(s)")
        for wire in nc_left:
            if dry_run:
                print(f"  would delete orphan NC wire {wire['primitiveId']} {wire.get('line')}")
            else:
                api_invoke(
                    "eda.sch_PrimitiveWire.delete",
                    [[wire["primitiveId"]]],
                    req_id,
                )
                req_id += 1

    if not dry_run and nc_left:
        wires_cache = api_invoke("eda.sch_PrimitiveWire.getAll", [], req_id)
        req_id += 1
        leftover = [w for w in (wires_cache if isinstance(wires_cache, list) else []) if w.get("net") == "NC"]
        print(f"NC wires after cleanup: {len(leftover)}")

    if not dry_run:
        saved = api_invoke("eda.sch_Document.save", [], req_id)
        print(f"save: {saved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove NC wires and set No Connect on DF17 NC pins")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--designator", help="Only U1 or U2")
    args = parser.parse_args()

    try:
        assign_nc_no_connect(dry_run=args.dry_run, only=args.designator)
    except Exception as exc:
        if "URLError" in type(exc).__name__ or "7655" in str(exc):
            print("无法连接 JLCEDA MCP (http://127.0.0.1:7655)。", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
