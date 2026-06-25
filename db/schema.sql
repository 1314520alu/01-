-- X9 Core DF17 引脚数据库
-- 编号约定：左上=1，左下=80；上行 1→40，下行 80→41

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    vendor      TEXT,
    notes       TEXT
);

CREATE TABLE IF NOT EXISTS connectors (
    id              INTEGER PRIMARY KEY,
    product_id      INTEGER NOT NULL REFERENCES products(id),
    part_number     TEXT NOT NULL UNIQUE,
    pin_count       INTEGER NOT NULL DEFAULT 80,
    pin1_corner     TEXT NOT NULL DEFAULT 'top_left',
    pin80_corner    TEXT NOT NULL DEFAULT 'bottom_left',
    top_row_order   TEXT NOT NULL DEFAULT 'LTR',
    bottom_row_order TEXT NOT NULL DEFAULT 'LTR',
    doc_path        TEXT,
    notes           TEXT
);

CREATE TABLE IF NOT EXISTS pins (
    id              INTEGER PRIMARY KEY,
    connector_id    INTEGER NOT NULL REFERENCES connectors(id),
    pin_number      INTEGER NOT NULL CHECK (pin_number BETWEEN 1 AND 80),
    signal_name     TEXT NOT NULL,
    category        TEXT,
    row             TEXT NOT NULL CHECK (row IN ('top', 'bottom')),
    row_position    INTEGER NOT NULL CHECK (row_position BETWEEN 1 AND 40),
    UNIQUE (connector_id, pin_number)
);

CREATE INDEX IF NOT EXISTS idx_pins_connector ON pins(connector_id);
CREATE INDEX IF NOT EXISTS idx_pins_signal ON pins(signal_name);
CREATE INDEX IF NOT EXISTS idx_pins_category ON pins(category);
