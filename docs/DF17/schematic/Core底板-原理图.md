# X9 Core 载板原理图（仅双 DF17）

> 自动生成：`python tools/setup_core_carrier_schematic.py`

## 页面

- **Sheet 名称**：`Core_Carrier`
- **标题**：X9 Core 载板 — 双 DF17 80P

## 视图镜像约定

Core 底视（上=80DS，下=80DP）：上排奇数 Pin1,3,…,79（左→右），下排偶数 Pin2,4,…,80（左→右）；四角 Pin1 左上、Pin2 左下、Pin79 右上、Pin80 右下。载板 PCB 为 Top View，相对 Core 底视左右 180° 镜像（载板 Pin1 在符号右上、Pin80 在左下）。载板 DP 配 Core DS（PCB +Y），载板 DS 配 Core DP（PCB −Y）。原理图页面与 Core 引脚图同序：上 J1=80DS、下 J2=80DP；载板标网取自 carrier-80DS/80DP 引脚表（同 Pin 号对接 Core 对面座子）。立创 LCSC 原符号为奇偶分行，使用工程库自定义符号 DF17-*-carrier-mirror。

## 与 Core 资料对照

| Core 底视位置 | Core 座子 | 载板位号 | 载板座子 | PCB |
|-------------|----------|----------|----------|-----|
| top | 80DS | J1 | DF17(3.0)-80DS-0.5V(57) | -Y |
| bottom | 80DP | J2 | DF17(1.0H)-80DP-0.5V(57) | +Y |

## 连接器

| 位号 | 载板位置 | 载板型号 | 对接 Core |
|------|----------|----------|-----------|
| J1 | -Y | DF17(3.0)-80DS-0.5V(57) | 80DP |
| J2 | +Y | DF17(1.0H)-80DP-0.5V(57) | 80DS |

## 引脚网络（按 Pin 编号）

### J1 — DF17(3.0)-80DS-0.5V(57)

| Pin | 网络名 | 类别 |
|-----|--------|------|
| 1 | CTS_TELEM3 | UART TELEM3 |
| 2 | VBUS | USB |
| 3 | RTS_TELEM3 | UART TELEM3 |
| 4 | VBUS | USB |
| 5 | RX_TELEM3 | UART TELEM3 |
| 6 | USB_D_N | USB |
| 7 | TX_TELEM3 | UART TELEM3 |
| 8 | USB_D_P | USB |
| 9 | CTS_TELEM2 | UART TELEM2 |
| 10 | GND | 地 |
| 11 | RTS_TELEM2 | UART TELEM2 |
| 12 | BUZZ- | 蜂鸣器 |
| 13 | RX_TELEM2 | UART TELEM2 |
| 14 | SAFETY_SW_LED | 安全开关 |
| 15 | TX_TELEM2 | UART TELEM2 |
| 16 | SAFETY_SW | 安全开关 |
| 17 | CTS_TELEM1 | UART TELEM1 |
| 18 | GND | 地 |
| 19 | RTS_TELEM1 | UART TELEM1 |
| 20 | NC | — |
| 21 | RX_TELEM1 | UART TELEM1 |
| 22 | VDD_5V_HIPOWER_nOC | 电源控制 |
| 23 | TX_TELEM1 | UART TELEM1 |
| 24 | VDD_5V_HIPOWER_nEN | 电源控制 |
| 25 | RX_GPS2 | UART GPS2 |
| 26 | VDD_5V_PERIPH_nOC | 电源控制 |
| 27 | TX_GPS2 | UART GPS2 |
| 28 | VDD_5V_PERIPH_nEN | 电源控制 |
| 29 | RX_GPS1 | UART GPS1 |
| 30 | PPM_IN_PORT | RC |
| 31 | TX_GPS1 | UART GPS1 |
| 32 | RSSI_IN_PORT | RC |
| 33 | RX_EXT2 | UART EXT2 |
| 34 | SBUS_OUTPUT_PORT | RC |
| 35 | TX_EXT2 | UART EXT2 |
| 36 | RX_SBUS_INPUT_PORT | RC |
| 37 | NC | — |
| 38 | GND | 地 |
| 39 | VDD_5V_IN | 电源 |
| 40 | VDD_5V_IN | 电源 |
| 41 | VDD_5V_IN | 电源 |
| 42 | VDD_5V_IN | 电源 |
| 43 | NC | — |
| 44 | GND | 地 |
| 45 | VDD_3V3_OUT | 电源 |
| 46 | ETH_LED | 以太网 |
| 47 | VDD_3V3_OUT | 电源 |
| 48 | GND | 地 |
| 49 | USART3_TX_DEBUG | 调试串口 |
| 50 | ETH_TD2_P | 以太网 |
| 51 | USART3_RX_DEBUG_P | 调试串口 |
| 52 | GND | 地 |
| 53 | FMU_SWDIO | SWD |
| 54 | ETH_TD2_N | 以太网 |
| 55 | FMU_SWCLK | SWD |
| 56 | GND | 地 |
| 57 | FMU_nRST | FMU |
| 58 | ETH_RD2_P | 以太网 |
| 59 | PD15(PH11) | GPIO |
| 60 | GND | 地 |
| 61 | NFC_GPIO | GPIO |
| 62 | ETH_RD2_N | 以太网 |
| 63 | GND | 地 |
| 64 | GND | 地 |
| 65 | FMU_CH1_PROT | PWM |
| 66 | NC | — |
| 67 | FMU_CH2_PROT | PWM |
| 68 | NC | — |
| 69 | FMU_CH3_PROT | PWM |
| 70 | NC | — |
| 71 | FMU_CH4_PROT | PWM |
| 72 | NC | — |
| 73 | FMU_CH5_PROT | PWM |
| 74 | NC | — |
| 75 | FMU_CH6_PROT | PWM |
| 76 | NC | — |
| 77 | FMU_CH7_PROT | PWM |
| 78 | NC | — |
| 79 | FMU_CH8_PROT | PWM |
| 80 | NC | — |

### J2 — DF17(1.0H)-80DP-0.5V(57)

| Pin | 网络名 | 类别 |
|-----|--------|------|
| 1 | SCK_EXT1 | SPI EXT1 |
| 2 | CAN2_N | CAN |
| 3 | MISO_EXT1 | SPI EXT1 |
| 4 | CAN2_P | CAN |
| 5 | MOSI_EXT1 | SPI EXT1 |
| 6 | CAN1_N | CAN |
| 7 | CS2_EXT1 | SPI EXT1 |
| 8 | CAN1_P | CAN |
| 9 | CS1_EXT1 | SPI EXT1 |
| 10 | GND | 地 |
| 11 | nSYNC_EXT1 | SPI EXT1 |
| 12 | nIO_LED_AMBER | LED |
| 13 | DRDY1_EXT1 | SPI EXT1 |
| 14 | nIO_LED_BLUE | LED |
| 15 | DRDY2_EXT1 | SPI EXT1 |
| 16 | NC | — |
| 17 | SPI_nRST | SPI EXT1 |
| 18 | GND | 地 |
| 19 | ADC3_6V6_PORT | ADC |
| 20 | SCL_GPS2 | I2C GPS2 |
| 21 | ADC3_3V3_PORT | ADC |
| 22 | SDA_GPS2 | I2C GPS2 |
| 23 | nARMED_PORT | FMU |
| 24 | SCL_GPS1 | I2C GPS1 |
| 25 | FMU_RST_REQ_PORT | FMU |
| 26 | SDA_GPS1 | I2C GPS1 |
| 27 | FMU_BOOTLOADER_PORT | FMU |
| 28 | SCL_EXT2 | I2C EXT2 |
| 29 | FMU_CAP1_PORT | FMU |
| 30 | SDA_EXT2 | I2C EXT2 |
| 31 | nLED_BLUE | LED |
| 32 | nPOWER_IN_C | 电源检测 |
| 33 | nLED_GREEN | LED |
| 34 | nPOWER_IN_B | 电源检测 |
| 35 | nLED_RED | LED |
| 36 | nPOWER_IN_A | 电源检测 |
| 37 | GND | 地 |
| 38 | NC | — |
| 39 | VDD_5V_IN | 电源 |
| 40 | VDD_5V_IN | 电源 |
| 41 | VDD_5V_IN | 电源 |
| 42 | VDD_5V_IN | 电源 |
| 43 | GND | 地 |
| 44 | NC | — |
| 45 | NC | — |
| 46 | VDD_SERVO_IN | 电源 |
| 47 | NC | — |
| 48 | NC | — |
| 49 | NC | — |
| 50 | IO_USART1_TX_DEBUG | 调试串口 |
| 51 | NC | — |
| 52 | IO_SWO | SWD |
| 53 | NC | — |
| 54 | IO_SWDIO | SWD |
| 55 | NC | — |
| 56 | IO_SWCLK | SWD |
| 57 | NC | — |
| 58 | IO_SPARE_GPIO1 | GPIO |
| 59 | NC | — |
| 60 | IO_SPARE_GPIO2 | GPIO |
| 61 | NC | — |
| 62 | IO_nRST | IO |
| 63 | NC | — |
| 64 | GND | 地 |
| 65 | GND | 地 |
| 66 | IO-CH8-PORT | PWM/IO |
| 67 | NC | — |
| 68 | IO-CH7-PORT | PWM/IO |
| 69 | NC | — |
| 70 | IO-CH6-PORT | PWM/IO |
| 71 | NC | — |
| 72 | IO-CH5-PORT | PWM/IO |
| 73 | NC | — |
| 74 | IO-CH4-PORT | PWM/IO |
| 75 | NC | — |
| 76 | IO-CH3-PORT | PWM/IO |
| 77 | NC | — |
| 78 | IO-CH2-PORT | PWM/IO |
| 79 | NC | — |
| 80 | IO-CH1-PORT | PWM/IO |

## EDA 操作步骤

1. 删除多余原理图页，仅保留一页并重命名为 Core_Carrier
2. 在工程库创建载板镜像符号（见 tools/create_df17_carrier_mirror_symbols.py）
3. 放置 J1=80DS（上）、J2=80DP（下），与 Core 官方引脚图同序；标网用 carrier-80DS/80DP 引脚表
4. LCSC 标准符号：J1(上 DS) rotation=90 mirror=true，J2(下 DP) rotation=270 mirror=true
5. （或 carrier-mirror 自定义符号：J1 rotation=0，J2 rotation=180）
6. Pin1 位于 J1 右上；J2 相对 J1 上下镜像（Pin1 左下）
7. PCB 贴装：+Y 仍为 80DP、−Y 仍为 80DS（与原理图上下顺序相反，属正常）
8. NC 引脚加 No Connect；GND 引脚后续统一接 GND 符号（手动）
9. PCB 导入 carrier-pcb.dxf 后替换 DXF 参考焊盘为官方封装
