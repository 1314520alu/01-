#!/usr/bin/env python3
"""将 DF17 引脚 Markdown 从旧编号（上1–40/下80–41）转为奇偶交错编号。

Core 底视：上排奇数 1,3,…,79（左→右），下排偶数 2,4,…,80（左→右）。
四角：Pin1 左上，Pin2 左下，Pin79 右上，Pin80 右下。
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINOUT_DIR = ROOT / "docs" / "DF17"
FILES = [
    PINOUT_DIR / "DF17-80DP-pinout.md",
    PINOUT_DIR / "DF17-80DS-pinout.md",
]

TABLE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)
PART_NUMBER_RE = re.compile(r"^\|\s*座子型号\s*\|\s*(.+?)\s*\|", re.MULTILINE)
TITLE_RE = re.compile(r"^# (.+?) 引脚定义", re.MULTILINE)
MATE_LINK_RE = re.compile(r"与 \[(.+?)\]\((.+?)\) 配对使用")

CONVENTION = """| 项目 | 说明 |
|------|------|
| 座子型号 | {part} |
| 引脚总数 | 80 |
| 编号约定 | **Core 底视**：上排奇数 Pin1,3,…,79（左→右）；下排偶数 Pin2,4,…,80（左→右） |
| 四角定位 | Pin1 左上 · Pin2 左下 · Pin79 右上 · Pin80 右下 |
| 载板 PCB | Top View，相对 Core 底视 **左右 180° 镜像**；载板 **DP 配 Core DS** |

> 飞控底部视图。载板侧连接器符号需镜像（Pin1 在载板符号右上，Pin80 在左下）。与 [{mate}]({mate_href}) 配对使用。"""


def parse_pins(path: Path) -> tuple[str, str, str, str, dict[int, tuple[str, str]]]:
    content = path.read_text(encoding="utf-8")
    part = PART_NUMBER_RE.search(content).group(1).strip()
    title = TITLE_RE.search(content).group(1)
    mate_m = MATE_LINK_RE.search(content)
    mate = mate_m.group(1) if mate_m else ""
    mate_href = mate_m.group(2) if mate_m else ""

    pins: dict[int, tuple[str, str]] = {}
    in_table = False
    for line in content.splitlines():
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
    return part, title, mate, mate_href, pins


def remap_old_sequential(pins: dict[int, tuple[str, str]]) -> dict[int, tuple[str, str]]:
    new: dict[int, tuple[str, str]] = {}
    for col in range(1, 41):
        new[2 * col - 1] = pins[col]
        new[2 * col] = pins[81 - col]
    return new


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


def pins_by_signal(pins: dict[int, tuple[str, str]], *signals: str) -> list[int]:
    sig_set = set(signals)
    return sorted(i for i, (s, _) in pins.items() if s in sig_set)


def pins_where(pins: dict[int, tuple[str, str]], pred) -> list[int]:
    return sorted(i for i, t in pins.items() if pred(t))


def format_pin_list(nums: list[int]) -> str:
    if not nums:
        return "—"
    parts: list[str] = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        parts.append(str(start) if start == prev else f"{start}–{prev}")
        start = prev = n
    parts.append(str(start) if start == prev else f"{start}–{prev}")
    return ", ".join(parts)


def pin_table(pins: dict[int, tuple[str, str]], nums: list[int]) -> list[str]:
    lines = ["| Pin | 信号名 |", "|-----|--------|"]
    for p in nums:
        lines.append(f"| {p} | {pins[p][0]} |")
    lines.append("")
    return lines


def render_groups(pins: dict[int, tuple[str, str]], is_dp: bool) -> list[str]:
    lines: list[str] = []
    gnd = pins_where(pins, lambda t: t[0] == "GND")
    nc = pins_where(pins, lambda t: t[0] == "NC")

    if is_dp:
        vdd5 = pins_by_signal(pins, "VDD_5V_IN")
        lines.extend([
            "### 电源",
            "",
            "| Pin | 信号名 | 说明 |",
            "|-----|--------|------|",
            f"| {format_pin_list(vdd5)} | VDD_5V_IN | 5 V 输入 |",
            f"| {format_pin_list(pins_by_signal(pins, 'VDD_3V3_OUT'))} | VDD_3V3_OUT | 3.3 V 输出 |",
            "| 67 | VDD_5V_PERIPH_nEN | 外设 5 V 使能 |",
            "| 68 | VDD_5V_PERIPH_nOC | 外设 5 V 过流 |",
            "| 69 | VDD_5V_HIPOWER_nEN | 大功率 5 V 使能 |",
            "| 70 | VDD_5V_HIPOWER_nOC | 大功率 5 V 过流 |",
            f"| {format_pin_list(pins_by_signal(pins, 'VBUS'))} | VBUS | USB 5 V |",
            "",
            "### 地（GND）",
            "",
            f"Pin：{format_pin_list(gnd)}",
            "",
            "### UART / 串口",
            "",
            "| 接口 | CTS | RTS | RX | TX |",
            "|------|-----|-----|----|----|",
            "| TELEM3 | 1 | 3 | 5 | 7 |",
            "| TELEM2 | 9 | 11 | 13 | 15 |",
            "| TELEM1 | 17 | 19 | 21 | 23 |",
            "| GPS2 | — | — | 25 | 27 |",
            "| GPS1 | — | — | 29 | 31 |",
            "| EXT2 | — | — | 33 | 35 |",
            f"| DEBUG | — | — | {pins_by_signal(pins, 'USART3_RX_DEBUG_P')[0]} | {pins_by_signal(pins, 'USART3_TX_DEBUG')[0]} |",
            "",
            "### FMU PWM 输出（带保护）",
            "",
            *pin_table(pins, pins_where(pins, lambda t: t[0].startswith("FMU_CH"))),
            "### 以太网（RGMII / PHY 相关）",
            "",
            *pin_table(pins, pins_where(pins, lambda t: t[0].startswith("ETH_"))),
            "### USB",
            "",
            *pin_table(
                pins,
                pins_where(pins, lambda t: t[0] in ("USB_D_P", "USB_D_N", "VBUS")),
            ),
            "### RC 输入 / 输出",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins,
                    lambda t: t[0]
                    in (
                        "RX_SBUS_INPUT_PORT",
                        "SBUS_OUTPUT_PORT",
                        "RSSI_IN_PORT",
                        "PPM_IN_PORT",
                    ),
                ),
            ),
            "### SWD 调试（FMU 侧）",
            "",
            *pin_table(
                pins,
                pins_where(pins, lambda t: t[0] in ("FMU_SWDIO", "FMU_SWCLK", "FMU_nRST")),
            ),
            "### 安全开关 / 蜂鸣器",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins, lambda t: t[0] in ("SAFETY_SW", "SAFETY_SW_LED", "BUZZ-")
                ),
            ),
            "### GPIO",
            "",
            *pin_table(
                pins,
                pins_where(pins, lambda t: t[0] in ("PD15(PH11)", "NFC_GPIO")),
            ),
        ])
    else:
        lines.extend([
            "### 电源",
            "",
            "| Pin | 信号名 | 说明 |",
            "|-----|--------|------|",
            f"| {format_pin_list(pins_by_signal(pins, 'VDD_5V_IN'))} | VDD_5V_IN | 5 V 输入 |",
            "| 58 | VDD_SERVO_IN | 舵机/外设 5 V 输入 |",
            "| 63 | nPOWER_IN_A | 电源输入检测 A |",
            "| 64 | nPOWER_IN_B | 电源输入检测 B |",
            "| 65 | nPOWER_IN_C | 电源输入检测 C |",
            "",
            "### 地（GND）",
            "",
            f"Pin：{format_pin_list(gnd)}",
            "",
            "### PWM / IO 通道",
            "",
            *pin_table(pins, pins_where(pins, lambda t: t[0].startswith("IO-CH"))),
            "### CAN 总线",
            "",
            *pin_table(
                pins,
                pins_where(pins, lambda t: t[0].startswith("CAN")),
            ),
            "### I2C",
            "",
            "| 总线 | SCL Pin | SDA Pin |",
            "|------|---------|---------|",
            f"| GPS1 | {pins_by_signal(pins, 'SCL_GPS1')[0]} | {pins_by_signal(pins, 'SDA_GPS1')[0]} |",
            f"| GPS2 | {pins_by_signal(pins, 'SCL_GPS2')[0]} | {pins_by_signal(pins, 'SDA_GPS2')[0]} |",
            f"| EXT2 | {pins_by_signal(pins, 'SCL_EXT2')[0]} | {pins_by_signal(pins, 'SDA_EXT2')[0]} |",
            "",
            "### SPI EXT1",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins,
                    lambda t: t[0]
                    in (
                        "SCK_EXT1",
                        "MISO_EXT1",
                        "MOSI_EXT1",
                        "CS2_EXT1",
                        "CS1_EXT1",
                        "nSYNC_EXT1",
                        "DRDY1_EXT1",
                        "DRDY2_EXT1",
                        "SPI_nRST",
                    ),
                ),
            ),
            "### SWD 调试（IO 侧）",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins,
                    lambda t: t[0]
                    in ("IO_SWCLK", "IO_SWDIO", "IO_SWO", "IO_USART1_TX_DEBUG"),
                ),
            ),
            "### FMU 控制 / 状态",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins,
                    lambda t: t[0]
                    in (
                        "ADC3_6V6_PORT",
                        "ADC3_3V3_PORT",
                        "nARMED_PORT",
                        "FMU_RST_REQ_PORT",
                        "FMU_BOOTLOADER_PORT",
                        "FMU_CAP1_PORT",
                    ),
                ),
            ),
            "### LED",
            "",
            "| Pin | 信号名 | 说明 |",
            "|-----|--------|------|",
            "| 16 | nLED_BLUE | FMU 蓝灯 |",
            "| 17 | nLED_GREEN | FMU 绿灯 |",
            "| 18 | nLED_RED | FMU 红灯 |",
            "| 74 | nIO_LED_BLUE | IO 蓝灯 |",
            "| 75 | nIO_LED_AMBER | IO 琥珀灯 |",
            "",
            "### GPIO / 复位",
            "",
            *pin_table(
                pins,
                pins_where(
                    pins,
                    lambda t: t[0]
                    in ("IO_nRST", "IO_SPARE_GPIO1", "IO_SPARE_GPIO2"),
                ),
            ),
        ])

    lines.extend([
        "### 未连接（NC）",
        "",
        f"Pin：{format_pin_list(nc)}",
        "",
    ])
    return lines


def write_pinout(path: Path, part: str, title: str, mate: str, mate_href: str, pins: dict[int, tuple[str, str]]) -> None:
    is_dp = "80DP" in path.name
    lines = [
        f"# {title} 引脚定义",
        "",
        CONVENTION.format(part=part, mate=mate, mate_href=mate_href),
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
        "## 功能分组",
        "",
        *render_groups(pins, is_dp),
        "---",
        "",
        "## 修订记录",
        "",
        "| 日期 | 说明 |",
        "|------|------|",
        "| 2026-06-25 | 从零一 X9 Core DF17 引脚图提取 |",
        "| 2026-06-25 | 编号改为奇偶交错：Pin1 左上、Pin2 左下、Pin79 右上、Pin80 右下 |",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for path in FILES:
        part, title, mate, mate_href, old = parse_pins(path)
        new = remap_old_sequential(old)
        write_pinout(path, part, title, mate, mate_href, new)
        print(f"Updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
