#!/usr/bin/env python3
"""生成 X9 Core 载板 PCB 用 DXF（Top View，可直接导入 EasyEDA PCB）。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Vec2

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "DF17" / "cad"
OUT_DXF = OUT_DIR / "carrier-pcb.dxf"

# --- 机械尺寸 (mm，与 Core 底面图一致) ---
CORE_HALF = 19.40
MOUNT_XY = 16.0
MOUNT_DIA = 2.50  # 载板 M2 螺丝孔（略大于 Core φ2.10）
CONN_CENTER_Y = 16.0
CONN_LEN_X = 24.0
CONN_HALF_X = CONN_LEN_X / 2
CONN_WIDTH_Y = 5.7  # Hirose 80pin 宽度

# 载板建议外形（可导入后改大）
CARRIER_HALF = 40.0
CARRIER_RADIUS = 3.0

# DF17 80pin 焊盘参考
DF17_PITCH = 0.5
DF17_ROW_PITCH = 3.0
DF17_PINS_PER_ROW = 40
DF17_CONTACT_SPAN = (DF17_PINS_PER_ROW - 1) * DF17_PITCH
DF17_PAD_R = 0.175


@dataclass(frozen=True)
class ConnectorSpec:
    cy: float
    carrier_part: str
    core_part: str
    gender: str


CONNECTORS = (
    ConnectorSpec(+CONN_CENTER_Y, "DF17(1.0H)-80DP-0.5V(57)", "DF17(3.0)-80DS-0.5V(57)", "DP"),
    ConnectorSpec(-CONN_CENTER_Y, "DF17(3.0)-80DS-0.5V(57)", "DF17(1.0H)-80DP-0.5V(57)", "DS"),
)


def rounded_rect_points(half_w: float, half_h: float, radius: float) -> list[Vec2]:
    r = min(radius, half_w, half_h)
    pts: list[Vec2] = []
    corners = [
        (half_w - r, half_h - r, 0),
        (-half_w + r, half_h - r, 90),
        (-half_w + r, -half_h + r, 180),
        (half_w - r, -half_h + r, 270),
    ]
    for cx, cy, start_deg in corners:
        for i in range(9):
            ang = math.radians(start_deg + i * (90 / 8))
            pts.append(Vec2(cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def add_layers(doc: ezdxf.document.Drawing) -> None:
    spec = {
        "BOARD_OUTLINE": 7,
        "CORE_KEEPOUT": 8,
        "DRILL": 1,
        "HOLE": 1,
        "FOOTPRINT": 4,
        "PAD": 2,
        "SILK_TOP": 7,
        "PIN1": 6,
        "REFERENCE": 140,
        "TEXT": 3,
    }
    for name, color in spec.items():
        doc.layers.add(name, color=color)
        if name == "REFERENCE":
            doc.layers.get(name).dxf.linetype = "DASHED"
        if name == "CORE_KEEPOUT":
            doc.layers.get(name).dxf.linetype = "DASHED"


def conn_box(cy: float) -> tuple[float, float, float, float]:
    return (
        -CONN_HALF_X,
        cy - CONN_WIDTH_Y / 2,
        CONN_HALF_X,
        cy + CONN_WIDTH_Y / 2,
    )


def add_df17_footprint(msp, spec: ConnectorSpec) -> None:
    """载板 Top 视图：Pin1 在连接器左上，上行 1→40 沿 +X。"""
    cy = spec.cy
    x_left = -DF17_CONTACT_SPAN / 2
    row_y = [cy + DF17_ROW_PITCH / 2, cy - DF17_ROW_PITCH / 2]

    for row_idx, py in enumerate(row_y):
        for i in range(DF17_PINS_PER_ROW):
            px = x_left + i * DF17_PITCH
            msp.add_circle((px, py), DF17_PAD_R, dxfattribs={"layer": "PAD"})

    x1, y1, x2, y2 = conn_box(cy)
    msp.add_lwpolyline(
        [(x1, y1), (x2, y1), (x2, y2), (x1, y2)],
        close=True,
        dxfattribs={"layer": "FOOTPRINT"},
    )

    pin1_x = x_left
    pin1_y = row_y[0]
    msp.add_circle((pin1_x, pin1_y), 0.4, dxfattribs={"layer": "PIN1"})
    msp.add_text("1", height=0.55, dxfattribs={"layer": "PIN1"}).set_placement(
        (pin1_x, pin1_y), align=TextEntityAlignment.MIDDLE_CENTER
    )

    label_y = y2 + 1.0 if cy > 0 else y1 - 1.6
    msp.add_text(
        f"{spec.carrier_part}  [{spec.gender}]",
        height=0.75,
        dxfattribs={"layer": "SILK_TOP"},
    ).set_placement((0, label_y), align=TextEntityAlignment.CENTER)
    msp.add_text(
        f"Core: {spec.core_part}",
        height=0.55,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, label_y - 1.1), align=TextEntityAlignment.CENTER)


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    add_layers(doc)
    msp = doc.modelspace()

    # 载板板框
    carrier_outline = rounded_rect_points(CARRIER_HALF, CARRIER_HALF, CARRIER_RADIUS)
    msp.add_lwpolyline(
        [(p.x, p.y) for p in carrier_outline],
        close=True,
        dxfattribs={"layer": "BOARD_OUTLINE"},
    )

    # Core 占位（虚线，勿放高元件）
    core_outline = rounded_rect_points(CORE_HALF, CORE_HALF, 3.0)
    msp.add_lwpolyline(
        [(p.x, p.y) for p in core_outline],
        close=True,
        dxfattribs={"layer": "CORE_KEEPOUT"},
    )

    # 四角安装孔（与 Core 32×32 对齐）
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        cx, cy = sx * MOUNT_XY, sy * MOUNT_XY
        msp.add_circle((cx, cy), MOUNT_DIA / 2, dxfattribs={"layer": "DRILL"})
        msp.add_circle((cx, cy), MOUNT_DIA / 2, dxfattribs={"layer": "HOLE"})

    # 两颗 DF17（载板侧 DS/DP 与 Core 配对）
    for spec in CONNECTORS:
        add_df17_footprint(msp, spec)

    # 中心对准
    msp.add_line((-CARRIER_HALF, 0), (CARRIER_HALF, 0), dxfattribs={"layer": "REFERENCE"})
    msp.add_line((0, -CARRIER_HALF), (0, CARRIER_HALF), dxfattribs={"layer": "REFERENCE"})

    msp.add_text(
        "X9 Core Carrier PCB — Top View",
        height=1.8,
        dxfattribs={"layer": "SILK_TOP"},
    ).set_placement((0, CARRIER_HALF - 3), align=TextEntityAlignment.CENTER)
    msp.add_text(
        "Origin (0,0) = Core/Carrier center | Pin1 top-left per connector",
        height=0.9,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, CARRIER_HALF - 5), align=TextEntityAlignment.CENTER)
    msp.add_text(
        "Top +Y: 80DP (mate Core 80DS)  |  Bottom -Y: 80DS (mate Core 80DP)",
        height=0.8,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, -CARRIER_HALF + 2.5), align=TextEntityAlignment.CENTER)

    doc.saveas(OUT_DXF)
    print(f"Wrote {OUT_DXF}")


if __name__ == "__main__":
    build()
