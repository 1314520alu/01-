#!/usr/bin/env python3
"""根据 X9 Core 底面机械图生成 DXF（原点 = 几何中心）。"""

from __future__ import annotations

import math
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Vec2

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "DF17" / "cad"
OUT_DXF = OUT_DIR / "X9-Core-bottom.dxf"

# --- 图纸标注尺寸 (mm) ---
BOARD_HALF = 19.40
MOUNT_XY = 16.0
MOUNT_DIA = 2.10
MOUNT_CB_DIA = 3.60
MOUNT_CB_DEPTH = 0.65

CONN_CENTER_X = 16.0
CONN_LEN_Y = 24.0  # 图纸标注
CONN_HALF_Y = CONN_LEN_Y / 2
CONN_WIDTH_X = 4.0  # 图纸示意宽度（壳体投影）

CENTER_RIB_HALF_W = 7.0  # 14 / 2
CENTER_RIB_H = 20.0

M2_DIA = 1.60
M2_POS = [
    (0.0, 0.0),
    (-8.0, 6.0),   # 图纸未标 Y，按底视图比例估算，导入后请核对
    (-8.0, -6.0),
]

# Hirose DF17-80 触点区（载板 footprint 参考，0.5mm pitch）
DF17_CONTACT_SPAN = 19.5
DF17_ROW_PITCH = 3.0
DF17_PITCH = 0.5
DF17_PINS_PER_ROW = 40


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


def add_poly(msp, layer: str, points: list[Vec2], close: bool = True) -> None:
    msp.add_lwpolyline(
        [(p.x, p.y) for p in points],
        close=close,
        dxfattribs={"layer": layer},
    )


def add_center_ribs(msp) -> None:
    slot_w = 1.0
    gap = 1.4
    x0 = -((5 * slot_w + 4 * gap) / 2) + slot_w / 2
    for i in range(5):
        x = x0 + i * (slot_w + gap)
        msp.add_lwpolyline(
            [
                (x - slot_w / 2, -CENTER_RIB_H / 2),
                (x + slot_w / 2, -CENTER_RIB_H / 2),
                (x + slot_w / 2, CENTER_RIB_H / 2),
                (x - slot_w / 2, CENTER_RIB_H / 2),
            ],
            close=True,
            dxfattribs={"layer": "CENTER_RIBS"},
        )


def connector_box(cx: float) -> tuple[float, float, float, float]:
    return (
        cx - CONN_WIDTH_X / 2,
        -CONN_HALF_Y,
        cx + CONN_WIDTH_X / 2,
        CONN_HALF_Y,
    )


def add_df17_pads(msp, cx: float, part: str) -> None:
    """在连接器区域绘制 80pin 0.5mm 焊盘参考（双列）。"""
    span = (DF17_PINS_PER_ROW - 1) * DF17_PITCH
    y_top = span / 2
    rows_x = [cx - DF17_ROW_PITCH / 2, cx + DF17_ROW_PITCH / 2]
    pad_r = 0.15
    for row_idx, px in enumerate(rows_x):
        for i in range(DF17_PINS_PER_ROW):
            py = y_top - i * DF17_PITCH
            msp.add_circle(
                (px, py),
                pad_r,
                dxfattribs={"layer": "DF17_PADS"},
            )
    x1, y1, x2, y2 = connector_box(cx)
    msp.add_text(
        part,
        height=0.8,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((cx, y2 + 1.2), align=TextEntityAlignment.CENTER)


def add_pin1_marker(msp, cx: float) -> None:
    x1, y1, _, y2 = connector_box(cx)
    msp.add_circle((x1 + 0.6, y2 - 0.6), 0.35, dxfattribs={"layer": "PIN1_MARK"})
    msp.add_text(
        "1",
        height=0.6,
        dxfattribs={"layer": "PIN1_MARK"},
    ).set_placement((x1 + 0.6, y2 - 0.6), align=TextEntityAlignment.MIDDLE_CENTER)


def add_dimensions(msp) -> None:
    def dim_h(y: float, x1: float, x2: float, label: str) -> None:
        msp.add_linear_dim(
            base=(0, y - 2.5),
            p1=(x1, y),
            p2=(x2, y),
            dimstyle="EZDXF",
            override={"dimtxt": 1.8, "layer": "DIM"},
        ).render()
        msp.add_text(label, height=1.5, dxfattribs={"layer": "TEXT"}).set_placement(
            ((x1 + x2) / 2, y - 4.5), align=TextEntityAlignment.CENTER
        )

    def dim_v(x: float, y1: float, y2: float, label: str) -> None:
        msp.add_linear_dim(
            base=(x - 2.5, 0),
            p1=(x, y1),
            p2=(x, y2),
            angle=90,
            dimstyle="EZDXF",
            override={"dimtxt": 1.8, "layer": "DIM"},
        ).render()
        msp.add_text(label, height=1.5, dxfattribs={"layer": "TEXT"}).set_placement(
            (x - 4.5, (y1 + y2) / 2), align=TextEntityAlignment.MIDDLE_CENTER
        )

    dim_h(-BOARD_HALF - 1, -BOARD_HALF, BOARD_HALF, "38.80")
    dim_v(-BOARD_HALF - 6, -BOARD_HALF, BOARD_HALF, "38.80")
    dim_h(BOARD_HALF + 3, -MOUNT_XY, MOUNT_XY, "32.00")
    dim_v(-BOARD_HALF - 10, -CONN_HALF_Y, CONN_HALF_Y, "24.00")
    dim_h(-BOARD_HALF - 10, -CONN_CENTER_X, 0, "16.00")


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()

    layers = {
        "OUTLINE": 7,
        "MOUNT_HOLES": 1,
        "MOUNT_CB": 3,
        "CONNECTOR": 4,
        "DF17_PADS": 8,
        "CENTER_RIBS": 9,
        "M2_HOLES": 6,
        "PIN1_MARK": 2,
        "TEXT": 7,
        "DIM": 5,
        "CENTERLINE": 140,
    }
    for name, color in layers.items():
        doc.layers.add(name, color=color)
        if name == "CENTERLINE":
            doc.layers.get(name).dxf.linetype = "CENTER"

    # 外轮廓（R3 圆角）
    outline = rounded_rect_points(BOARD_HALF, BOARD_HALF, 3.0)
    add_poly(msp, "OUTLINE", outline)

    # 安装孔
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        cx, cy = sx * MOUNT_XY, sy * MOUNT_XY
        msp.add_circle((cx, cy), MOUNT_CB_DIA / 2, dxfattribs={"layer": "MOUNT_CB"})
        msp.add_circle((cx, cy), MOUNT_DIA / 2, dxfattribs={"layer": "MOUNT_HOLES"})
        msp.add_text(
            f"φ{MOUNT_DIA}贯穿\nφ{MOUNT_CB_DIA}↓{MOUNT_CB_DEPTH}",
            height=0.7,
            dxfattribs={"layer": "TEXT"},
        ).set_placement((cx + 2.2, cy + 2.2))

    # 两颗 DF17 投影
    for cx, part in ((-CONN_CENTER_X, "DF17(3.0)-80DS"), (CONN_CENTER_X, "DF17(1.0H)-80DP")):
        x1, y1, x2, y2 = connector_box(cx)
        msp.add_lwpolyline(
            [(x1, y1), (x2, y1), (x2, y2), (x1, y2)],
            close=True,
            dxfattribs={"layer": "CONNECTOR"},
        )
        add_df17_pads(msp, cx, part)
        add_pin1_marker(msp, cx)

    add_center_ribs(msp)

    for x, y in M2_POS:
        msp.add_circle((x, y), M2_DIA / 2, dxfattribs={"layer": "M2_HOLES"})
    msp.add_text(
        "3×φ1.60 ↓3  /  M2-6H ↓3",
        height=0.7,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((-8, -9.5))

    # 中心线
    msp.add_line((-BOARD_HALF - 5, 0), (BOARD_HALF + 5, 0), dxfattribs={"layer": "CENTERLINE"})
    msp.add_line((0, -BOARD_HALF - 5), (0, BOARD_HALF + 5), dxfattribs={"layer": "CENTERLINE"})

    msp.add_text(
        "X9 Core 底面视图（Bottom View）",
        height=2.0,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, BOARD_HALF + 6), align=TextEntityAlignment.CENTER)
    msp.add_text(
        "Pin1 约定：连接器左上=1，左下=80",
        height=1.2,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, BOARD_HALF + 4), align=TextEntityAlignment.CENTER)
    msp.add_text(
        "M2 孔位 Y 向为估算值，请以官方 DXF 复核",
        height=1.0,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, -BOARD_HALF - 6), align=TextEntityAlignment.CENTER)

    try:
        add_dimensions(msp)
    except Exception:
        pass

    doc.saveas(OUT_DXF)
    print(f"Wrote {OUT_DXF}")


if __name__ == "__main__":
    build()
