#!/usr/bin/env python3
"""X9 Core 载板 — 单页原理图规格（仅两颗 80P DF17）。

载板 Top View（见 docs/DF17/cad/carrier-pcb.dxf）：
  J1 (+Y)  DF17(1.0H)-80DP  对接 X9 Core 底部 80DS
  J2 (−Y)  DF17(3.0)-80DS  对接 X9 Core 底部 80DP

原理图仅放置上述两颗连接器；各引脚以网络标签/引脚名标注，暂不画外设。
引脚数据来自 db/pinout.db。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "pinout.db"
OUT_DIR = ROOT / "docs" / "DF17" / "schematic"

CONNECTORS = [
    {
        "designator": "J1",
        "part_number": "DF17(1.0H)-80DP-0.5V(57)",
        "name": "MATE_CORE_80DS",
        "position": "+Y",
        "core_ref": "80DS",
        "core_doc_position": "top",
        "mates_core": "80DS",
        "schematic_x": 80,
        "schematic_y": 60,
        "rotation": 180,
        "mirror": False,
    },
    {
        "designator": "J2",
        "part_number": "DF17(3.0)-80DS-0.5V(57)",
        "name": "MATE_CORE_80DP",
        "position": "-Y",
        "core_ref": "80DP",
        "core_doc_position": "bottom",
        "mates_core": "80DP",
        "schematic_x": 80,
        "schematic_y": 420,
        "rotation": 180,
        "mirror": False,
    },
]

VIEW_CONVENTION = (
    "Core 资料为飞控 Bottom View：Pin1 左上、Pin80 左下（上排1→40，下排80→41）。"
    "载板原理图目标：Pin1 右上、Pin80 右下（Core 左右镜像）。"
    "立创 LCSC 原符号为奇偶分行，无法靠 rotation 同时满足；"
    "使用工程库自定义符号 DF17-*-carrier-mirror（见 create_df17_carrier_mirror_symbols.py）。"
)

PAGE = {
    "name": "Core_Carrier",
    "title": "X9 Core 载板 — 双 DF17 80P",
    "note": "载板侧连接器需镜像反向（零一官方说明）。本页仅 Core 对接座，不含外设。",
}


def load_pins(conn: sqlite3.Connection, part_number: str) -> list[dict]:
    rows = conn.execute(
        """
        SELECT p.pin_number, p.signal_name, p.category, p.row, p.row_position
        FROM pins p
        JOIN connectors c ON c.id = p.connector_id
        WHERE c.part_number = ?
        ORDER BY p.pin_number
        """,
        (part_number,),
    ).fetchall()
    return [
        {
            "pin": r[0],
            "net": r[1],
            "category": r[2],
            "row": r[3],
            "row_pos": r[4],
        }
        for r in rows
    ]


def build_spec() -> dict:
    conn = sqlite3.connect(DB_PATH)
    try:
        connectors = []
        for item in CONNECTORS:
            pins = load_pins(conn, item["part_number"])
            connectors.append({**item, "pins": pins})
    finally:
        conn.close()

    return {
        "project": "01飞控",
        "viewConvention": VIEW_CONVENTION,
        "page": PAGE,
        "connectors": connectors,
        "eda_steps": [
            "删除多余原理图页，仅保留一页并重命名为 Core_Carrier",
            "在工程库创建载板镜像符号（见 tools/create_df17_carrier_mirror_symbols.py）",
            "放置 J1=80DP @ +Y、J2=80DS @ −Y，使用 carrier-mirror 符号，rotation=0",
            "Pin1 位于连接器右上、Pin80 右下（与 Core 底视左右镜像一致）",
            "NC 引脚加 No Connect；GND 引脚后续统一接 GND 符号（手动）",
            "PCB 导入 carrier-pcb.dxf 后替换 DXF 参考焊盘为官方封装",
        ],
        "mcp_api_sequence": [
            {
                "step": "rename_page",
                "api": "eda.dmt_Schematic.modifySchematicPageName",
                "args_note": "[pageUuid, 'Core_Carrier']",
            },
            {
                "step": "title_text",
                "api": "eda.sch_PrimitiveText.create",
                "args": [50, 30, PAGE["title"], 0, None, None, 14, True],
            },
            {
                "step": "note_text",
                "api": "eda.sch_PrimitiveText.create",
                "args": [50, 55, PAGE["note"], 0, None, None, 10, False],
            },
            {
                "step": "place_j1_j2",
                "api": "eda.sch_PrimitiveComponent.create",
                "args_note": "需 component_select 确认 uuid/libraryUuid 后放置",
            },
        ],
    }


def write_markdown(spec: dict, path: Path) -> None:
    lines = [
        "# X9 Core 载板原理图（仅双 DF17）",
        "",
        "> 自动生成：`python tools/setup_core_carrier_schematic.py`",
        "",
        "## 页面",
        "",
        f"- **Sheet 名称**：`{PAGE['name']}`",
        f"- **标题**：{PAGE['title']}",
        "",
        "## 视图镜像约定",
        "",
        spec.get("viewConvention", VIEW_CONVENTION),
        "",
        "## 与 Core 资料对照",
        "",
        "| Core 底视位置 | Core 座子 | 载板位号 | 载板座子 | PCB |",
        "|-------------|----------|----------|----------|-----|",
    ]
    for c in spec["connectors"]:
        lines.append(
            f"| {c.get('core_doc_position', '—')} | {c.get('core_ref', c['mates_core'])} | "
            f"{c['designator']} | {c['part_number']} | {c['position']} |"
        )
    lines.extend(["", "## 连接器", "", "| 位号 | 载板位置 | 载板型号 | 对接 Core |", "|------|----------|----------|-----------|"])
    for c in spec["connectors"]:
        lines.append(
            f"| {c['designator']} | {c['position']} | {c['part_number']} | {c['mates_core']} |"
        )

    lines.extend(["", "## 引脚网络（按 Pin 编号）", ""])
    for c in spec["connectors"]:
        lines.append(f"### {c['designator']} — {c['part_number']}")
        lines.append("")
        lines.append("| Pin | 网络名 | 类别 |")
        lines.append("|-----|--------|------|")
        for p in c["pins"]:
            cat = p["category"] or "—"
            lines.append(f"| {p['pin']} | {p['net']} | {cat} |")
        lines.append("")

    lines.extend(["## EDA 操作步骤", ""])
    for i, step in enumerate(spec["eda_steps"], 1):
        lines.append(f"{i}. {step}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    spec = build_spec()
    json_path = OUT_DIR / "core-carrier-schematic-spec.json"
    md_path = OUT_DIR / "Core底板-原理图.md"
    json_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(spec, md_path)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Connectors: {', '.join(c['designator'] for c in spec['connectors'])}")


if __name__ == "__main__":
    main()
