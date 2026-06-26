#!/usr/bin/env python3
"""从 Core 引脚表生载板侧 Pin↔网络 Markdown。

载板网络取自 **对接 Core 座子** 的引脚表（同 Pin 号，镜像贴装后对接）：
  - 载板 80DS（−Y）← Core 80DP
  - 载板 80DP（+Y）← Core 80DS
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINOUT_DIR = ROOT / "docs" / "DF17"

CORE_DS = PINOUT_DIR / "DF17-80DS-pinout.md"
CORE_DP = PINOUT_DIR / "DF17-80DP-pinout.md"

TABLE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)

CARRIER_SPECS = [
    {
        "out": PINOUT_DIR / "carrier-80DS-pinout.md",
        "part_number": "DF17(3.0)-80DS-0.5V(57)",
        "pcb_position": "−Y",
        "mates_core": "80DP",
        "net_source": CORE_DP,
        "net_source_label": "Core 80DP",
    },
    {
        "out": PINOUT_DIR / "carrier-80DP-pinout.md",
        "part_number": "DF17(1.0H)-80DP-0.5V(57)",
        "pcb_position": "+Y",
        "mates_core": "80DS",
        "net_source": CORE_DS,
        "net_source_label": "Core 80DS",
    },
]


def parse_pins(path: Path) -> dict[int, tuple[str, str]]:
    pins: dict[int, tuple[str, str]] = {}
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 完整引脚表"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table:
            continue
        row = TABLE_ROW_RE.match(line)
        if not row:
            continue
        for pin_str, signal, category in (
            (row.group(1), row.group(2).strip(), row.group(3).strip()),
            (row.group(4), row.group(5).strip(), row.group(6).strip()),
        ):
            pins[int(pin_str)] = (signal, category)
    if len(pins) != 80:
        raise ValueError(f"{path.name}: expected 80 pins, got {len(pins)}")
    return pins


def table_rows(pins: dict[int, tuple[str, str]]) -> list[str]:
    lines = [
        "| Pin | 信号名 | 类别 | Pin | 信号名 | 类别 |",
        "|-----|--------|------|-----|--------|------|",
    ]
    for n in range(1, 81, 2):
        s1, c1 = pins[n]
        s2, c2 = pins[n + 1]
        lines.append(f"| {n} | {s1} | {c1} | {n + 1} | {s2} | {c2} |")
    return lines


def row_grid_top(pins: dict[int, tuple[str, str]]) -> list[str]:
    lines: list[str] = []
    odds = [pins[i][0] for i in range(1, 80, 2)]
    for start in range(0, 40, 10):
        chunk = odds[start : start + 10]
        nums = list(range(start * 2 + 1, start * 2 + 1 + 2 * len(chunk), 2))
        lines.append("| " + " | ".join(str(n) for n in nums) + " |")
        lines.append("|" + "|".join("---" for _ in nums) + "|")
        lines.append("| " + " | ".join(chunk) + " |")
        lines.append("")
    return lines


def row_grid_bottom(pins: dict[int, tuple[str, str]]) -> list[str]:
    lines: list[str] = []
    nums_lr = list(range(80, 0, -2))
    sigs_lr = [pins[i][0] for i in nums_lr]
    for start in range(0, 40, 10):
        nchunk = nums_lr[start : start + 10]
        schunk = sigs_lr[start : start + 10]
        lines.append("| " + " | ".join(str(n) for n in nchunk) + " |")
        lines.append("|" + "|".join("---" for _ in nchunk) + "|")
        lines.append("| " + " | ".join(schunk) + " |")
        lines.append("")
    return lines


def render(spec: dict, pins: dict[int, tuple[str, str]]) -> str:
    mate_link = "DF17-80DP-pinout.md" if spec["mates_core"] == "80DP" else "DF17-80DS-pinout.md"
    src_link = spec["net_source"].name
    lines = [
        f"# 载板 {spec['part_number']} 引脚定义",
        "",
        "| 项目 | 说明 |",
        "|------|------|",
        "| 角色 | **载板** |",
        f"| 座子型号 | {spec['part_number']} |",
        "| 引脚总数 | 80 |",
        f"| 载板位置 | PCB **{spec['pcb_position']}** |",
        f"| 对接 Core | **{spec['mates_core']}** |",
        f"| 网络来源 | 同 Pin 号取自 [{spec['net_source_label']}]({src_link}) |",
        "| 编号约定 | 上排奇数 Pin1,3,…,79（左→右）；下排偶数 Pin2,4,…,80（左→右） |",
        "| 载板 Top View | Pin1 **右上** · Pin2 **右下** · Pin79 **左上** · Pin80 **左下**（相对 Core 底视左右 180° 镜像） |",
        "",
        f"> 载板原理图/PCB 标网用本表。Core 侧定义见 [{spec['mates_core']}]({mate_link})。",
        "",
        "---",
        "",
        "## 完整引脚表（Pin 1–80）",
        "",
        *table_rows(pins),
        "",
        "---",
        "",
        "## 按行排列（便于对照丝印）",
        "",
        "### 上排奇数 Pin 1,3,…,79（左 → 右）",
        "",
        *row_grid_top(pins),
        "### 下排偶数 Pin 80,78,…,2（左 = 80，右 = 2）",
        "",
        *row_grid_bottom(pins),
        "---",
        "",
        "## 修订记录",
        "",
        "| 日期 | 说明 |",
        "|------|------|",
        "| 2026-06-25 | 由 Core 引脚表交叉映射生成（载板 DS←Core DP，载板 DP←Core DS） |",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    for spec in CARRIER_SPECS:
        source_pins = parse_pins(spec["net_source"])
        spec["out"].write_text(render(spec, source_pins), encoding="utf-8")
        print(f"Wrote {spec['out'].relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc
