# DF17(1.0H)-80DP-0.5V(57) 引脚定义

| 项目 | 说明 |
|------|------|
| 座子型号 | DF17(1.0H)-80DP-0.5V(57) |
| 引脚总数 | 80 |
| 编号约定 | **Core 底视**：左上=Pin1，左下=Pin80 · **载板原理图（rot180）**：右上=Pin1，左下=Pin80（右下=Pin79，见说明） |
| 上行 | Pin 1 → 40，自左向右 |
| 下行 | Pin 80 → 41，自左向右 |

> 飞控底部视图；载板侧连接器需镜像反向。与 [80DS 座子](DF17-80DS-pinout.md) 配对使用。

---

## 完整引脚表（Pin 1–80）

| Pin | 信号名 | 类别 | Pin | 信号名 | 类别 |
|-----|--------|------|-----|--------|------|
| 1 | CTS_TELEM3 | UART TELEM3 | 41 | NC | — |
| 2 | RTS_TELEM3 | UART TELEM3 | 42 | NC | — |
| 3 | RX_TELEM3 | UART TELEM3 | 43 | NC | — |
| 4 | TX_TELEM3 | UART TELEM3 | 44 | NC | — |
| 5 | CTS_TELEM2 | UART TELEM2 | 45 | NC | — |
| 6 | RTS_TELEM2 | UART TELEM2 | 46 | NC | — |
| 7 | RX_TELEM2 | UART TELEM2 | 47 | NC | — |
| 8 | TX_TELEM2 | UART TELEM2 | 48 | NC | — |
| 9 | CTS_TELEM1 | UART TELEM1 | 49 | GND | 地 |
| 10 | RTS_TELEM1 | UART TELEM1 | 50 | ETH_RD2_N | 以太网 |
| 11 | RX_TELEM1 | UART TELEM1 | 51 | GND | 地 |
| 12 | TX_TELEM1 | UART TELEM1 | 52 | ETH_RD2_P | 以太网 |
| 13 | RX_GPS2 | UART GPS2 | 53 | GND | 地 |
| 14 | TX_GPS2 | UART GPS2 | 54 | ETH_TD2_N | 以太网 |
| 15 | RX_GPS1 | UART GPS1 | 55 | GND | 地 |
| 16 | TX_GPS1 | UART GPS1 | 56 | ETH_TD2_P | 以太网 |
| 17 | RX_EXT2 | UART EXT2 | 57 | GND | 地 |
| 18 | TX_EXT2 | UART EXT2 | 58 | ETH_LED | 以太网 |
| 19 | NC | — | 59 | GND | 地 |
| 20 | VDD_5V_IN | 电源 | 60 | VDD_5V_IN | 电源 |
| 21 | VDD_5V_IN | 电源 | 61 | VDD_5V_IN | 电源 |
| 22 | NC | — | 62 | GND | 地 |
| 23 | VDD_3V3_OUT | 电源 | 63 | RX_SBUS_INPUT_PORT | RC |
| 24 | VDD_3V3_OUT | 电源 | 64 | SBUS_OUTPUT_PORT | RC |
| 25 | USART3_TX_DEBUG | 调试串口 | 65 | RSSI_IN_PORT | RC |
| 26 | USART3_RX_DEBUG_P | 调试串口 | 66 | PPM_IN_PORT | RC |
| 27 | FMU_SWDIO | SWD | 67 | VDD_5V_PERIPH_nEN | 电源控制 |
| 28 | FMU_SWCLK | SWD | 68 | VDD_5V_PERIPH_nOC | 电源控制 |
| 29 | FMU_nRST | FMU | 69 | VDD_5V_HIPOWER_nEN | 电源控制 |
| 30 | PD15(PH11) | GPIO | 70 | VDD_5V_HIPOWER_nOC | 电源控制 |
| 31 | NFC_GPIO | GPIO | 71 | NC | — |
| 32 | GND | 地 | 72 | GND | 地 |
| 33 | FMU_CH1_PROT | PWM | 73 | SAFETY_SW | 安全开关 |
| 34 | FMU_CH2_PROT | PWM | 74 | SAFETY_SW_LED | 安全开关 |
| 35 | FMU_CH3_PROT | PWM | 75 | BUZZ- | 蜂鸣器 |
| 36 | FMU_CH4_PROT | PWM | 76 | GND | 地 |
| 37 | FMU_CH5_PROT | PWM | 77 | USB_D_P | USB |
| 38 | FMU_CH6_PROT | PWM | 78 | USB_D_N | USB |
| 39 | FMU_CH7_PROT | PWM | 79 | VBUS | USB |
| 40 | FMU_CH8_PROT | PWM | 80 | VBUS | USB |

---

## 按行排列（便于对照丝印）

### 上行 Pin 1–40（左 → 右）

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| CTS_TELEM3 | RTS_TELEM3 | RX_TELEM3 | TX_TELEM3 | CTS_TELEM2 | RTS_TELEM2 | RX_TELEM2 | TX_TELEM2 | CTS_TELEM1 | RTS_TELEM1 |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|----|----|----|----|----|----|----|----|----|-----|
| RX_TELEM1 | TX_TELEM1 | RX_GPS2 | TX_GPS2 | RX_GPS1 | TX_GPS1 | RX_EXT2 | TX_EXT2 | NC | VDD_5V_IN |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|----|----|----|----|----|----|----|----|----|-----|
| VDD_5V_IN | NC | VDD_3V3_OUT | VDD_3V3_OUT | USART3_TX_DEBUG | USART3_RX_DEBUG_P | FMU_SWDIO | FMU_SWCLK | FMU_nRST | PD15(PH11) |

| 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|----|----|----|----|----|----|----|----|----|-----|
| NFC_GPIO | GND | FMU_CH1_PROT | FMU_CH2_PROT | FMU_CH3_PROT | FMU_CH4_PROT | FMU_CH5_PROT | FMU_CH6_PROT | FMU_CH7_PROT | FMU_CH8_PROT |

### 下行 Pin 80–41（左 = 80，右 = 41）

| 80 | 79 | 78 | 77 | 76 | 75 | 74 | 73 | 72 | 71 |
|----|----|----|----|----|----|----|----|----|-----|
| VBUS | VBUS | USB_D_N | USB_D_P | GND | BUZZ- | SAFETY_SW_LED | SAFETY_SW | GND | NC |

| 70 | 69 | 68 | 67 | 66 | 65 | 64 | 63 | 62 | 61 |
|----|----|----|----|----|----|----|----|----|-----|
| VDD_5V_HIPOWER_nOC | VDD_5V_HIPOWER_nEN | VDD_5V_PERIPH_nOC | VDD_5V_PERIPH_nEN | PPM_IN_PORT | RSSI_IN_PORT | SBUS_OUTPUT_PORT | RX_SBUS_INPUT_PORT | GND | VDD_5V_IN |

| 60 | 59 | 58 | 57 | 56 | 55 | 54 | 53 | 52 | 51 |
|----|----|----|----|----|----|----|----|----|-----|
| VDD_5V_IN | GND | ETH_LED | GND | ETH_TD2_P | GND | ETH_TD2_N | GND | ETH_RD2_P | GND |

| 50 | 49 | 48 | 47 | 46 | 45 | 44 | 43 | 42 | 41 |
|----|----|----|----|----|----|----|----|----|-----|
| ETH_RD2_N | GND | NC | NC | NC | NC | NC | NC | NC | NC |

---

## 功能分组

### 电源

| Pin | 信号名 | 说明 |
|-----|--------|------|
| 20, 21, 60, 61 | VDD_5V_IN | 5 V 输入 |
| 23, 24 | VDD_3V3_OUT | 3.3 V 输出 |
| 67 | VDD_5V_PERIPH_nEN | 外设 5 V 使能 |
| 68 | VDD_5V_PERIPH_nOC | 外设 5 V 过流 |
| 69 | VDD_5V_HIPOWER_nEN | 大功率 5 V 使能 |
| 70 | VDD_5V_HIPOWER_nOC | 大功率 5 V 过流 |
| 79, 80 | VBUS | USB 5 V |

### 地（GND）

Pin：**32, 49, 51, 53, 55, 57, 59, 62, 72, 76**

### UART / 串口

| 接口 | CTS | RTS | RX | TX |
|------|-----|-----|----|----|
| TELEM3 | 1 | 2 | 3 | 4 |
| TELEM2 | 5 | 6 | 7 | 8 |
| TELEM1 | 9 | 10 | 11 | 12 |
| GPS2 | — | — | 13 | 14 |
| GPS1 | — | — | 15 | 16 |
| EXT2 | — | — | 17 | 18 |
| DEBUG | — | — | 26 | 25 |

### FMU PWM 输出（带保护）

| Pin | 信号名 |
|-----|--------|
| 33 | FMU_CH1_PROT |
| 34 | FMU_CH2_PROT |
| 35 | FMU_CH3_PROT |
| 36 | FMU_CH4_PROT |
| 37 | FMU_CH5_PROT |
| 38 | FMU_CH6_PROT |
| 39 | FMU_CH7_PROT |
| 40 | FMU_CH8_PROT |

### 以太网（RGMII / PHY 相关）

| Pin | 信号名 |
|-----|--------|
| 50 | ETH_RD2_N |
| 52 | ETH_RD2_P |
| 54 | ETH_TD2_N |
| 56 | ETH_TD2_P |
| 58 | ETH_LED |

### USB

| Pin | 信号名 |
|-----|--------|
| 77 | USB_D_P |
| 78 | USB_D_N |
| 79, 80 | VBUS |

### RC 输入 / 输出

| Pin | 信号名 |
|-----|--------|
| 63 | RX_SBUS_INPUT_PORT |
| 64 | SBUS_OUTPUT_PORT |
| 65 | RSSI_IN_PORT |
| 66 | PPM_IN_PORT |

### SWD 调试（FMU 侧）

| Pin | 信号名 |
|-----|--------|
| 27 | FMU_SWDIO |
| 28 | FMU_SWCLK |
| 29 | FMU_nRST |

### 安全开关 / 蜂鸣器

| Pin | 信号名 |
|-----|--------|
| 73 | SAFETY_SW |
| 74 | SAFETY_SW_LED |
| 75 | BUZZ- |

### GPIO

| Pin | 信号名 |
|-----|--------|
| 30 | PD15(PH11) |
| 31 | NFC_GPIO |

### 未连接（NC）

Pin：**19, 22, 41–48, 71**

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-25 | 从零一 X9 Core DF17 引脚图提取，约定左上=1、左下=80 |
