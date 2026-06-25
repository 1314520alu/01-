#!/usr/bin/env python3
"""从 docs/DF17/*.md 导入引脚表到 SQLite。"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "pinout.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"
PINOUT_FILES = [
    ROOT / "docs" / "DF17" / "DF17-80DS-pinout.md",
    ROOT / "docs" / "DF17" / "DF17-80DP-pinout.md",
]

TABLE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)
PART_NUMBER_RE = re.compile(r"^\|\s*座子型号\s*\|\s*(.+?)\s*\|", re.MULTILINE)


def row_info(pin_number: int) -> tuple[str, int]:
    if pin_number <= 40:
        return "top", pin_number
    return "bottom", 81 - pin_number


def normalize_category(raw: str) -> str | None:
    value = raw.strip()
    if not value or value == "—":
        return None
    return value


def parse_markdown(path: Path) -> tuple[str, list[dict]]:
    content = path.read_text(encoding="utf-8")
    match = PART_NUMBER_RE.search(content)
    if not match:
        raise ValueError(f"未找到座子型号: {path}")

    part_number = match.group(1).strip()
    pins: dict[int, dict] = {}

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

        for pin_str, signal, category, pin2_str, signal2, category2 in (
            (row.group(1), row.group(2), row.group(3), row.group(4), row.group(5), row.group(6)),
        ):
            for pin_number, sig, cat in (
                (int(pin_str), signal.strip(), category),
                (int(pin2_str), signal2.strip(), category2),
            ):
                row_name, row_position = row_info(pin_number)
                pins[pin_number] = {
                    "pin_number": pin_number,
                    "signal_name": sig,
                    "category": normalize_category(cat),
                    "row": row_name,
                    "row_position": row_position,
                }

    if len(pins) != 80:
        missing = sorted(set(range(1, 81)) - set(pins))
        raise ValueError(f"{path.name} 引脚不完整，缺少: {missing[:10]}{'...' if len(missing) > 10 else ''}")

    ordered = [pins[i] for i in range(1, 81)]
    return part_number, ordered


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def upsert_data(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        INSERT INTO products (name, vendor, notes)
        VALUES ('X9 Core', '零一飞行', 'ArduPilot 飞控')
        ON CONFLICT(name) DO UPDATE SET vendor=excluded.vendor, notes=excluded.notes
        """
    )
    product_id = conn.execute("SELECT id FROM products WHERE name = 'X9 Core'").fetchone()[0]

    for md_path in PINOUT_FILES:
        part_number, pins = parse_markdown(md_path)
        rel_doc = md_path.relative_to(ROOT).as_posix()

        conn.execute(
            """
            INSERT INTO connectors (
                product_id, part_number, pin_count, doc_path,
                pin1_corner, pin80_corner, top_row_order, bottom_row_order,
                notes
            )
            VALUES (?, ?, 80, ?, 'top_left', 'bottom_left', 'LTR', 'LTR', ?)
            ON CONFLICT(part_number) DO UPDATE SET
                product_id=excluded.product_id,
                doc_path=excluded.doc_path,
                notes=excluded.notes
            """,
            (
                product_id,
                part_number,
                rel_doc,
                "飞控底部视图；载板侧需镜像反向",
            ),
        )
        connector_id = conn.execute(
            "SELECT id FROM connectors WHERE part_number = ?", (part_number,)
        ).fetchone()[0]

        conn.execute("DELETE FROM pins WHERE connector_id = ?", (connector_id,))
        conn.executemany(
            """
            INSERT INTO pins (
                connector_id, pin_number, signal_name, category, row, row_position
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    connector_id,
                    pin["pin_number"],
                    pin["signal_name"],
                    pin["category"],
                    pin["row"],
                    pin["row_position"],
                )
                for pin in pins
            ],
        )


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        init_db(conn)
        upsert_data(conn)
        conn.commit()

        summary = conn.execute(
            """
            SELECT c.part_number, COUNT(p.id) AS pin_count
            FROM connectors c
            JOIN pins p ON p.connector_id = c.id
            GROUP BY c.id
            ORDER BY c.part_number
            """
        ).fetchall()

    print(f"数据库: {DB_PATH}")
    for row in summary:
        print(f"  {row['part_number']}: {row['pin_count']} pins")


if __name__ == "__main__":
    main()
