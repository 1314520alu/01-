#!/usr/bin/env python3
"""从 docs/DF17/*.md 导入引脚表到 SQLite（Core + 载板）。"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "pinout.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"
PINOUT_DIR = ROOT / "docs" / "DF17"

TABLE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)
PART_NUMBER_RE = re.compile(r"^\|\s*座子型号\s*\|\s*(.+?)\s*\|", re.MULTILINE)
ROLE_RE = re.compile(r"^\|\s*角色\s*\|\s*\**(.+?)\**\s*\|", re.MULTILINE)
PCB_POSITION_RE = re.compile(r"^\|\s*载板位置\s*\|\s*PCB\s*\**(.+?)\**\s*\|", re.MULTILINE)
MATES_CORE_RE = re.compile(r"^\|\s*对接 Core\s*\|\s*\**(.+?)\**\s*\|", re.MULTILINE)

MATES_CORE_TO_PART = {
    "80DS": "DF17(3.0)-80DS-0.5V(57)",
    "80DP": "DF17(1.0H)-80DP-0.5V(57)",
}

PINOUT_FILES = [
    PINOUT_DIR / "DF17-80DS-pinout.md",
    PINOUT_DIR / "DF17-80DP-pinout.md",
    PINOUT_DIR / "carrier-80DS-pinout.md",
    PINOUT_DIR / "carrier-80DP-pinout.md",
]


@dataclass
class PinoutMeta:
    part_number: str
    role: str
    product_name: str
    pcb_position: str | None
    mates_part_number: str | None
    pin1_corner: str
    pin80_corner: str
    notes: str


def row_info(pin_number: int) -> tuple[str, int]:
    if pin_number % 2 == 1:
        return "top", (pin_number + 1) // 2
    return "bottom", pin_number // 2


def normalize_category(raw: str) -> str | None:
    value = raw.strip()
    if not value or value == "—":
        return None
    return value


def parse_role(raw: str | None) -> str:
    if not raw:
        return "core"
    text = raw.strip().lower()
    if "载板" in raw or text == "carrier":
        return "carrier"
    return "core"


def parse_meta(path: Path) -> PinoutMeta:
    content = path.read_text(encoding="utf-8")
    part_number = PART_NUMBER_RE.search(content).group(1).strip()
    role = parse_role(ROLE_RE.search(content).group(1) if ROLE_RE.search(content) else None)

    pcb_position = None
    mates_part_number = None
    if role == "carrier":
        pcb_m = PCB_POSITION_RE.search(content)
        if pcb_m:
            pcb_position = pcb_m.group(1).strip()
        mates_m = MATES_CORE_RE.search(content)
        if mates_m:
            mates_part_number = MATES_CORE_TO_PART.get(mates_m.group(1).strip(), mates_m.group(1).strip())
        pin1_corner = "top_right"
        pin80_corner = "bottom_left"
        product_name = "X9 Carrier"
        notes = "载板 Top View；网络取自对接 Core 座子同 Pin 号"
    else:
        pin1_corner = "top_left"
        pin80_corner = "bottom_right"
        product_name = "X9 Core"
        notes = "Core 底视奇偶交错编号"

    return PinoutMeta(
        part_number=part_number,
        role=role,
        product_name=product_name,
        pcb_position=pcb_position,
        mates_part_number=mates_part_number,
        pin1_corner=pin1_corner,
        pin80_corner=pin80_corner,
        notes=notes,
    )


def parse_pins(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8")
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
        for pin_str, signal, category in (
            (row.group(1), row.group(2), row.group(3)),
            (row.group(4), row.group(5), row.group(6)),
        ):
            pin_number = int(pin_str)
            row_name, row_position = row_info(pin_number)
            pins[pin_number] = {
                "pin_number": pin_number,
                "signal_name": signal.strip(),
                "category": normalize_category(category),
                "row": row_name,
                "row_position": row_position,
            }

    if len(pins) != 80:
        missing = sorted(set(range(1, 81)) - set(pins))
        raise ValueError(f"{path.name} 引脚不完整，缺少: {missing[:10]}{'...' if len(missing) > 10 else ''}")
    return [pins[i] for i in range(1, 81)]


def connector_columns(conn: sqlite3.Connection) -> set[str]:
    return {row[1] for row in conn.execute("PRAGMA table_info(connectors)")}


def migrate_connectors_table(conn: sqlite3.Connection) -> None:
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    if "connectors_new" in tables:
        conn.execute("DROP TABLE connectors_new")

    if "connectors" not in tables:
        return

    cols = connector_columns(conn)
    if "role" in cols:
        return

    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.executescript(
            """
            CREATE TABLE connectors_new (
                id                INTEGER PRIMARY KEY,
                product_id        INTEGER NOT NULL REFERENCES products(id),
                part_number       TEXT NOT NULL,
                role              TEXT NOT NULL DEFAULT 'core'
                                      CHECK (role IN ('core', 'carrier')),
                pin_count         INTEGER NOT NULL DEFAULT 80,
                pin1_corner       TEXT NOT NULL DEFAULT 'top_left',
                pin80_corner      TEXT NOT NULL DEFAULT 'bottom_right',
                top_row_order     TEXT NOT NULL DEFAULT 'LTR',
                bottom_row_order  TEXT NOT NULL DEFAULT 'LTR',
                pcb_position      TEXT,
                mates_part_number TEXT,
                doc_path          TEXT,
                notes             TEXT,
                UNIQUE (part_number, role)
            );
            INSERT INTO connectors_new (
                id, product_id, part_number, role, pin_count,
                pin1_corner, pin80_corner, top_row_order, bottom_row_order,
                pcb_position, mates_part_number, doc_path, notes
            )
            SELECT
                id, product_id, part_number, 'core', pin_count,
                pin1_corner, pin80_corner, top_row_order, bottom_row_order,
                NULL, NULL, doc_path, notes
            FROM connectors;
            DROP TABLE connectors;
            ALTER TABLE connectors_new RENAME TO connectors;
            CREATE INDEX IF NOT EXISTS idx_connectors_role ON connectors(role);
            """
        )
    finally:
        conn.execute("PRAGMA foreign_keys = ON")


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    migrate_connectors_table(conn)


def upsert_product(conn: sqlite3.Connection, name: str, notes: str) -> int:
    conn.execute(
        """
        INSERT INTO products (name, vendor, notes)
        VALUES (?, '零一飞行', ?)
        ON CONFLICT(name) DO UPDATE SET notes=excluded.notes
        """,
        (name, notes),
    )
    return conn.execute("SELECT id FROM products WHERE name = ?", (name,)).fetchone()[0]


def upsert_data(conn: sqlite3.Connection) -> None:
    for md_path in PINOUT_FILES:
        if not md_path.exists():
            raise FileNotFoundError(f"缺少引脚文档: {md_path}（先运行 tools/generate_carrier_pinout_md.py）")

        meta = parse_meta(md_path)
        pins = parse_pins(md_path)
        rel_doc = md_path.relative_to(ROOT).as_posix()
        product_id = upsert_product(
            conn,
            meta.product_name,
            "多旋翼载板" if meta.role == "carrier" else "ArduPilot 飞控",
        )

        conn.execute(
            """
            INSERT INTO connectors (
                product_id, part_number, role, pin_count, doc_path,
                pin1_corner, pin80_corner, top_row_order, bottom_row_order,
                pcb_position, mates_part_number, notes
            )
            VALUES (?, ?, ?, 80, ?, ?, ?, 'LTR', 'LTR', ?, ?, ?)
            ON CONFLICT(part_number, role) DO UPDATE SET
                product_id=excluded.product_id,
                doc_path=excluded.doc_path,
                pin1_corner=excluded.pin1_corner,
                pin80_corner=excluded.pin80_corner,
                pcb_position=excluded.pcb_position,
                mates_part_number=excluded.mates_part_number,
                notes=excluded.notes
            """,
            (
                product_id,
                meta.part_number,
                meta.role,
                rel_doc,
                meta.pin1_corner,
                meta.pin80_corner,
                meta.pcb_position,
                meta.mates_part_number,
                meta.notes,
            ),
        )
        connector_id = conn.execute(
            "SELECT id FROM connectors WHERE part_number = ? AND role = ?",
            (meta.part_number, meta.role),
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
            SELECT c.part_number, c.role, COUNT(p.id) AS pin_count
            FROM connectors c
            JOIN pins p ON p.connector_id = c.id
            GROUP BY c.id
            ORDER BY c.role, c.part_number
            """
        ).fetchall()

    print(f"数据库: {DB_PATH}")
    for row in summary:
        print(f"  [{row['role']}] {row['part_number']}: {row['pin_count']} pins")


if __name__ == "__main__":
    main()
