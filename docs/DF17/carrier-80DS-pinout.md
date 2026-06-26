# 载板 DF17(3.0)-80DS-0.5V(57) 引脚定义

| 项目 | 说明 |
|------|------|
| 角色 | **载板** |
| 座子型号 | DF17(3.0)-80DS-0.5V(57) |
| 引脚总数 | 80 |
| 载板位置 | PCB **−Y** |
| 对接 Core | **80DP** |
| 网络来源 | 同 Pin 号取自 [Core 80DP](DF17-80DP-pinout.md) |
| 编号约定 | 上排奇数 Pin1,3,…,79（左→右）；下排偶数 Pin2,4,…,80（左→右） |
| 载板 Top View | Pin1 **右上** · Pin2 **右下** · Pin79 **左上** · Pin80 **左下**（相对 Core 底视左右 180° 镜像） |

> 载板原理图/PCB 标网用本表。Core 侧定义见 [80DP](DF17-80DP-pinout.md)。

---

## 完整引脚表（Pin 1–80）

| Pin | 信号名 | 类别 | Pin | 信号名 | 类别 |
|-----|--------|------|-----|--------|------|
| 1 | CTS_TELEM3 | UART TELEM3 | 2 | VBUS | USB |
| 3 | RTS_TELEM3 | UART TELEM3 | 4 | VBUS | USB |
| 5 | RX_TELEM3 | UART TELEM3 | 6 | USB_D_N | USB |
| 7 | TX_TELEM3 | UART TELEM3 | 8 | USB_D_P | USB |
| 9 | CTS_TELEM2 | UART TELEM2 | 10 | GND | 地 |
| 11 | RTS_TELEM2 | UART TELEM2 | 12 | BUZZ- | 蜂鸣器 |
| 13 | RX_TELEM2 | UART TELEM2 | 14 | SAFETY_SW_LED | 安全开关 |
| 15 | TX_TELEM2 | UART TELEM2 | 16 | SAFETY_SW | 安全开关 |
| 17 | CTS_TELEM1 | UART TELEM1 | 18 | GND | 地 |
| 19 | RTS_TELEM1 | UART TELEM1 | 20 | NC | — |
| 21 | RX_TELEM1 | UART TELEM1 | 22 | VDD_5V_HIPOWER_nOC | 电源控制 |
| 23 | TX_TELEM1 | UART TELEM1 | 24 | VDD_5V_HIPOWER_nEN | 电源控制 |
| 25 | RX_GPS2 | UART GPS2 | 26 | VDD_5V_PERIPH_nOC | 电源控制 |
| 27 | TX_GPS2 | UART GPS2 | 28 | VDD_5V_PERIPH_nEN | 电源控制 |
| 29 | RX_GPS1 | UART GPS1 | 30 | PPM_IN_PORT | RC |
| 31 | TX_GPS1 | UART GPS1 | 32 | RSSI_IN_PORT | RC |
| 33 | RX_EXT2 | UART EXT2 | 34 | SBUS_OUTPUT_PORT | RC |
| 35 | TX_EXT2 | UART EXT2 | 36 | RX_SBUS_INPUT_PORT | RC |
| 37 | NC | — | 38 | GND | 地 |
| 39 | VDD_5V_IN | 电源 | 40 | VDD_5V_IN | 电源 |
| 41 | VDD_5V_IN | 电源 | 42 | VDD_5V_IN | 电源 |
| 43 | NC | — | 44 | GND | 地 |
| 45 | VDD_3V3_OUT | 电源 | 46 | ETH_LED | 以太网 |
| 47 | VDD_3V3_OUT | 电源 | 48 | GND | 地 |
| 49 | USART3_TX_DEBUG | 调试串口 | 50 | ETH_TD2_P | 以太网 |
| 51 | USART3_RX_DEBUG_P | 调试串口 | 52 | GND | 地 |
| 53 | FMU_SWDIO | SWD | 54 | ETH_TD2_N | 以太网 |
| 55 | FMU_SWCLK | SWD | 56 | GND | 地 |
| 57 | FMU_nRST | FMU | 58 | ETH_RD2_P | 以太网 |
| 59 | PD15(PH11) | GPIO | 60 | GND | 地 |
| 61 | NFC_GPIO | GPIO | 62 | ETH_RD2_N | 以太网 |
| 63 | GND | 地 | 64 | GND | 地 |
| 65 | FMU_CH1_PROT | PWM | 66 | NC | — |
| 67 | FMU_CH2_PROT | PWM | 68 | NC | — |
| 69 | FMU_CH3_PROT | PWM | 70 | NC | — |
| 71 | FMU_CH4_PROT | PWM | 72 | NC | — |
| 73 | FMU_CH5_PROT | PWM | 74 | NC | — |
| 75 | FMU_CH6_PROT | PWM | 76 | NC | — |
| 77 | FMU_CH7_PROT | PWM | 78 | NC | — |
| 79 | FMU_CH8_PROT | PWM | 80 | NC | — |

---

## 按行排列（便于对照丝印）

### 上排奇数 Pin 1,3,…,79（左 → 右）

| 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 |
|---|---|---|---|---|---|---|---|---|---|
| CTS_TELEM3 | RTS_TELEM3 | RX_TELEM3 | TX_TELEM3 | CTS_TELEM2 | RTS_TELEM2 | RX_TELEM2 | TX_TELEM2 | CTS_TELEM1 | RTS_TELEM1 |

| 21 | 23 | 25 | 27 | 29 | 31 | 33 | 35 | 37 | 39 |
|---|---|---|---|---|---|---|---|---|---|
| RX_TELEM1 | TX_TELEM1 | RX_GPS2 | TX_GPS2 | RX_GPS1 | TX_GPS1 | RX_EXT2 | TX_EXT2 | NC | VDD_5V_IN |

| 41 | 43 | 45 | 47 | 49 | 51 | 53 | 55 | 57 | 59 |
|---|---|---|---|---|---|---|---|---|---|
| VDD_5V_IN | NC | VDD_3V3_OUT | VDD_3V3_OUT | USART3_TX_DEBUG | USART3_RX_DEBUG_P | FMU_SWDIO | FMU_SWCLK | FMU_nRST | PD15(PH11) |

| 61 | 63 | 65 | 67 | 69 | 71 | 73 | 75 | 77 | 79 |
|---|---|---|---|---|---|---|---|---|---|
| NFC_GPIO | GND | FMU_CH1_PROT | FMU_CH2_PROT | FMU_CH3_PROT | FMU_CH4_PROT | FMU_CH5_PROT | FMU_CH6_PROT | FMU_CH7_PROT | FMU_CH8_PROT |

### 下排偶数 Pin 80,78,…,2（左 = 80，右 = 2）

| 80 | 78 | 76 | 74 | 72 | 70 | 68 | 66 | 64 | 62 |
|---|---|---|---|---|---|---|---|---|---|
| NC | NC | NC | NC | NC | NC | NC | NC | GND | ETH_RD2_N |

| 60 | 58 | 56 | 54 | 52 | 50 | 48 | 46 | 44 | 42 |
|---|---|---|---|---|---|---|---|---|---|
| GND | ETH_RD2_P | GND | ETH_TD2_N | GND | ETH_TD2_P | GND | ETH_LED | GND | VDD_5V_IN |

| 40 | 38 | 36 | 34 | 32 | 30 | 28 | 26 | 24 | 22 |
|---|---|---|---|---|---|---|---|---|---|
| VDD_5V_IN | GND | RX_SBUS_INPUT_PORT | SBUS_OUTPUT_PORT | RSSI_IN_PORT | PPM_IN_PORT | VDD_5V_PERIPH_nEN | VDD_5V_PERIPH_nOC | VDD_5V_HIPOWER_nEN | VDD_5V_HIPOWER_nOC |

| 20 | 18 | 16 | 14 | 12 | 10 | 8 | 6 | 4 | 2 |
|---|---|---|---|---|---|---|---|---|---|
| NC | GND | SAFETY_SW | SAFETY_SW_LED | BUZZ- | GND | USB_D_P | USB_D_N | VBUS | VBUS |

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-25 | 由 Core 引脚表交叉映射生成（载板 DS←Core DP，载板 DP←Core DS） |
