#!/usr/bin/env python3
"""X9 Core 载板 — 单页原理图规格（仅两颗 80P DF17）。

载板 PCB Top View（见 docs/DF17/cad/carrier-pcb.dxf）：
  +Y  DF17(1.0H)-80DP  对接 Core 80DS
  −Y  DF17(3.0)-80DS  对接 Core 80DP

原理图页面布局与 Core 官方引脚图一致（上 80DS、下 80DP），便于对照；
各座子标网取自 **载板引脚表**（载板 DS←Core DP，载板 DP←Core DS，见 carrier-*.md）。
引脚数据来自 db/pinout.db（role=carrier）。
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
        "part_number": "DF17(3.0)-80DS-0.5V(57)",
        "name": "CORE_80DS_TOP",
        "position": "-Y",
        "carrier_pcb": "-Y",
        "core_ref": "80DS",
        "core_doc_position": "top",
        "mates_core": "80DP",
        "schematic_x": 80,
        "schematic_y": 420,
        "rotation": 90,
        "mirror": True,
    },
    {
        "designator": "J2",
        "part_number": "DF17(1.0H)-80DP-0.5V(57)",
        "name": "CORE_80DP_BOTTOM",
        "position": "+Y",
        "carrier_pcb": "+Y",
        "core_ref": "80DP",
        "core_doc_position": "bottom",
        "mates_core": "80DS",
        "schematic_x": 80,
        "schematic_y": 60,
        "rotation": 270,
        "mirror": True,
    },
]

VIEW_CONVENTION = (
    "Core 底视（上=80DS，下=80DP）：上排奇数 Pin1,3,…,79（左→右），下排偶数 Pin2,4,…,80（左→右）；"
    "四角 Pin1 左上、Pin2 左下、Pin79 右上、Pin80 右下。"
    "载板 PCB 为 Top View，相对 Core 底视左右 180° 镜像（载板 Pin1 在符号右上、Pin80 在左下）。"
    "载板 DP 配 Core DS（PCB +Y），载板 DS 配 Core DP（PCB −Y）。"
    "原理图页面与 Core 引脚图同序：上 J1=80DS、下 J2=80DP；"
    "载板标网取自 carrier-80DS/80DP 引脚表（同 Pin 号对接 Core 对面座子）。"
    "立创 LCSC 原符号为奇偶分行，使用工程库自定义符号 DF17-*-carrier-mirror。"
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
        WHERE c.part_number = ? AND c.role = 'carrier'
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
            "放置 J1=80DS（上）、J2=80DP（下），与 Core 官方引脚图同序；标网用 carrier-80DS/80DP 引脚表",
            "LCSC 标准符号：J1(上 DS) rotation=90 mirror=true，J2(下 DP) rotation=270 mirror=true",
            "（或 carrier-mirror 自定义符号：J1 rotation=0，J2 rotation=180）",
            "Pin1 位于 J1 右上；J2 相对 J1 上下镜像（Pin1 左下）",
            "PCB 贴装：+Y 仍为 80DP、−Y 仍为 80DS（与原理图上下顺序相反，属正常）",
            "运行 tools/assign_core_carrier_nets.py --replace 标网（NC 默认跳过）",
            "运行 tools/assign_nc_no_connect.py 删除 NC 导线；No Connect（×）若 MCP 未生效则 EDA 内手动",
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
