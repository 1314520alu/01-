#!/usr/bin/env python3
"""在工程库创建 DF17 载板镜像符号（Core 底视左右镜像布局）。

目标布局（水平放置，信号引脚朝上/下）::

    79  77  ...  3   1     ← 上排奇数，Pin1 在右上（载板镜像 Core 左上）
    80  78  ...  4   2     ← 下排偶数，Pin2 在右下（载板镜像 Core 左下）

Core 底视：Pin1 左上、Pin2 左下、Pin79 右上、Pin80 右下。
载板 Top View 左右 180° 镜像后：Pin1 右上、Pin2 右下、Pin79 左上、Pin80 左下。

立创 LCSC 原符号亦为奇偶分行，但默认 Pin1 方位与载板镜像目标不一致时需工程库自定义符号。

用法：嘉立创 EDA Bridge 连接后，由 Agent 通过 MCP api_invoke 逐步执行本脚本
输出的 JSON 步骤；或手动在符号编辑器按 PIN_LAYOUT 放置引脚。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "DF17" / "schematic" / "df17-carrier-mirror-symbol-steps.json"

# 源符号（立创 LCSC 库，与当前 J1/J2 一致）
SOURCE_SYMBOLS = {
    "80DP": {
        "symbolUuid": "aacd252d459658c7",
        "libraryUuid": "4297f1465aa64d66b16af1faf5416d0b",
        "deviceUuid": "e6705924e6ed3dc5",
        "deviceLibraryUuid": "176f93f9fa8e444e9152cfea941f0716",
        "footprintUuid": "41014d676388e9b3",
        "footprintLibraryUuid": "11d64e09bf6d49a69a9ff4c79f03007d",
        "newSymbolName": "DF17-80DP-carrier-mirror",
        "newDeviceName": "DF17-80DP-carrier-mirror",
    },
    "80DS": {
        "symbolUuid": "4b5cf0754c5b827f",
        "libraryUuid": "5e386959b89145bb99e7b30e7f347b38",
        "deviceUuid": "9793f502e118ff4b",
        "deviceLibraryUuid": "b51f303c81fa48c2af5e1e3914fe31dd",
        "footprintUuid": "26191b657f4ba01e",
        "footprintLibraryUuid": "7959c201ad8f414db07dc6f76415daaf",
        "newSymbolName": "DF17-80DS-carrier-mirror",
        "newDeviceName": "DF17-80DS-carrier-mirror",
    },
}

# 符号几何（单位：mil，与 EDA 默认一致）
COLS = 40
COL_PITCH = 10
ROW_GAP = 20
PIN_LEN = 10
ORIGIN_X = 0
ORIGIN_Y = 0


def pin_layout() -> list[dict]:
    """载板镜像引脚坐标：col 0 = 最右列（Pin1 / Pin2 侧）。"""
    pins: list[dict] = []
    right_x = ORIGIN_X + (COLS - 1) * COL_PITCH
    for col in range(COLS):
        x = right_x - col * COL_PITCH
        top_pin = 2 * col + 1
        bottom_pin = 2 * col + 2
        pins.append(
            {
                "pinNumber": str(top_pin),
                "x": x,
                "y": ORIGIN_Y,
                "rotation": 270,
            }
        )
        pins.append(
            {
                "pinNumber": str(bottom_pin),
                "x": x,
                "y": ORIGIN_Y + ROW_GAP,
                "rotation": 90,
            }
        )
    # 金属壳/安装 Pin81、82（与原符号一致，左右侧）
    pins.extend(
        [
            {"pinNumber": "81", "x": ORIGIN_X - 15, "y": ORIGIN_Y + ROW_GAP // 2, "rotation": 0},
            {"pinNumber": "82", "x": right_x + 15, "y": ORIGIN_Y + ROW_GAP // 2, "rotation": 180},
        ]
    )
    return pins


def build_mcp_steps() -> list[dict]:
    steps: list[dict] = [
        {
            "step": "get_project_library",
            "api": "eda.lib_LibrariesList.getProjectLibraryUuid",
            "args": [],
            "save_as": "projectLibUuid",
        },
    ]
    for key, src in SOURCE_SYMBOLS.items():
        tag = key.lower()
        steps.extend(
            [
                {
                    "step": f"copy_symbol_{tag}",
                    "api": "eda.lib_Symbol.copy",
                    "args": [
                        src["symbolUuid"],
                        src["libraryUuid"],
                        "${projectLibUuid}",
                        None,
                        src["newSymbolName"],
                    ],
                    "save_as": f"newSymbolUuid_{tag}",
                },
                {
                    "step": f"open_symbol_{tag}",
                    "api": "eda.lib_Symbol.openInEditor",
                    "args": [f"${{newSymbolUuid_{tag}}}", "${projectLibUuid}"],
                    "note": "打开符号编辑器后，删除原引脚，按 pin_layout 重建",
                },
                {
                    "step": f"copy_device_{tag}",
                    "api": "eda.lib_Device.copy",
                    "args": [
                        src["deviceUuid"],
                        src["deviceLibraryUuid"],
                        "${projectLibUuid}",
                        None,
                        src["newDeviceName"],
                    ],
                    "save_as": f"newDeviceUuid_{tag}",
                },
                {
                    "step": f"bind_symbol_{tag}",
                    "api": "eda.lib_Device.modify",
                    "args": [
                        f"${{newDeviceUuid_{tag}}}",
                        "${projectLibUuid}",
                        src["newDeviceName"],
                        None,
                        {
                            "symbolUuid": f"${{newSymbolUuid_{tag}}}",
                            "symbol": {
                                "uuid": f"${{newSymbolUuid_{tag}}}",
                                "libraryUuid": "${projectLibUuid}",
                            },
                            "footprintUuid": src["footprintUuid"],
                            "footprint": {
                                "uuid": src["footprintUuid"],
                                "libraryUuid": src["footprintLibraryUuid"],
                            },
                        },
                    ],
                },
            ]
        )
    steps.extend(
        [
            {
                "step": "place_j1",
                "api": "eda.sch_PrimitiveComponent.create",
                "args": [
                    {"libraryUuid": "${projectLibUuid}", "uuid": "${newDeviceUuid_80dp}"},
                    120,
                    100,
                    None,
                    0,
                    False,
                    True,
                    True,
                ],
                "then_modify": {
                    "designator": "J1",
                    "name": "MATE_CORE_80DS",
                },
            },
            {
                "step": "place_j2",
                "api": "eda.sch_PrimitiveComponent.create",
                "args": [
                    {"libraryUuid": "${projectLibUuid}", "uuid": "${newDeviceUuid_80ds}"},
                120,
                320,
                None,
                180,
                False,
                True,
                True,
            ],
                "then_modify": {
                    "designator": "J2",
                    "name": "MATE_CORE_80DP",
                },
            },
        ]
    )
    return steps


def main() -> None:
    payload = {
        "description": "DF17 载板镜像符号 — MCP 执行步骤",
        "pinLayout": pin_layout(),
        "sourceSymbols": SOURCE_SYMBOLS,
        "mcpSteps": build_mcp_steps(),
        "symbolEditorNotes": [
            "复制符号后 openInEditor，在符号编辑器内用 sch_PrimitivePin.create 按 pinLayout 放置 82 个引脚",
            "sch_PrimitivePin.create(x, y, pinNumber, pinNumber, rotation, pinLength)",
            "画矩形外框连接两排引脚；Pin1 圆点标在右上角",
            "J1 carrier-mirror：rotation=0 mirror=false；J2 carrier-mirror：rotation=180 mirror=false",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Pin layout: {len(payload['pinLayout'])} pins")


if __name__ == "__main__":
    main()
