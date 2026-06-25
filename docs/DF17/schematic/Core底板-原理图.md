# X9 Core 载板原理图（仅双 DF17）

> 自动生成：`python tools/setup_core_carrier_schematic.py`

## 页面

- **Sheet 名称**：`Core_Carrier`
- **标题**：X9 Core 载板 — 双 DF17 80P

## 视图镜像约定

Core 资料为飞控 Bottom View（上=80DS，下=80DP，Pin1 左上）。载板原理图/PCB 为 Top View 镜像：同物理边对应 Core 资料，载板用相反公母（+Y=80DP 接 Core80DS，−Y=80DS 接 Core80DP），符号 rotation=180 + mirror=true。

## 与 Core 资料对照

| Core 底视位置 | Core 座子 | 载板位号 | 载板座子 | PCB |
|-------------|----------|----------|----------|-----|
| top | 80DS | J1 | DF17(1.0H)-80DP-0.5V(57) | +Y |
| bottom | 80DP | J2 | DF17(3.0)-80DS-0.5V(57) | -Y |

## 连接器

| 位号 | 载板位置 | 载板型号 | 对接 Core |
|------|----------|----------|-----------|
| J1 | +Y | DF17(1.0H)-80DP-0.5V(57) | 80DS |
| J2 | -Y | DF17(3.0)-80DS-0.5V(57) | 80DP |

## 引脚网络（按 Pin 编号）

### J1 — DF17(1.0H)-80DP-0.5V(57)

| Pin | 网络名 | 类别 |
|-----|--------|------|
| 1 | CTS_TELEM3 | UART TELEM3 |
| 2 | RTS_TELEM3 | UART TELEM3 |
| 3 | RX_TELEM3 | UART TELEM3 |
| 4 | TX_TELEM3 | UART TELEM3 |
| 5 | CTS_TELEM2 | UART TELEM2 |
| 6 | RTS_TELEM2 | UART TELEM2 |
| 7 | RX_TELEM2 | UART TELEM2 |
| 8 | TX_TELEM2 | UART TELEM2 |
| 9 | CTS_TELEM1 | UART TELEM1 |
| 10 | RTS_TELEM1 | UART TELEM1 |
| 11 | RX_TELEM1 | UART TELEM1 |
| 12 | TX_TELEM1 | UART TELEM1 |
| 13 | RX_GPS2 | UART GPS2 |
| 14 | TX_GPS2 | UART GPS2 |
| 15 | RX_GPS1 | UART GPS1 |
| 16 | TX_GPS1 | UART GPS1 |
| 17 | RX_EXT2 | UART EXT2 |
| 18 | TX_EXT2 | UART EXT2 |
| 19 | NC | — |
| 20 | VDD_5V_IN | 电源 |
| 21 | VDD_5V_IN | 电源 |
| 22 | NC | — |
| 23 | VDD_3V3_OUT | 电源 |
| 24 | VDD_3V3_OUT | 电源 |
| 25 | USART3_TX_DEBUG | 调试串口 |
| 26 | USART3_RX_DEBUG_P | 调试串口 |
| 27 | FMU_SWDIO | SWD |
| 28 | FMU_SWCLK | SWD |
| 29 | FMU_nRST | FMU |
| 30 | PD15(PH11) | GPIO |
| 31 | NFC_GPIO | GPIO |
| 32 | GND | 地 |
| 33 | FMU_CH1_PROT | PWM |
| 34 | FMU_CH2_PROT | PWM |
| 35 | FMU_CH3_PROT | PWM |
| 36 | FMU_CH4_PROT | PWM |
| 37 | FMU_CH5_PROT | PWM |
| 38 | FMU_CH6_PROT | PWM |
| 39 | FMU_CH7_PROT | PWM |
| 40 | FMU_CH8_PROT | PWM |
| 41 | NC | — |
| 42 | NC | — |
| 43 | NC | — |
| 44 | NC | — |
| 45 | NC | — |
| 46 | NC | — |
| 47 | NC | — |
| 48 | NC | — |
| 49 | GND | 地 |
| 50 | ETH_RD2_N | 以太网 |
| 51 | GND | 地 |
| 52 | ETH_RD2_P | 以太网 |
| 53 | GND | 地 |
| 54 | ETH_TD2_N | 以太网 |
| 55 | GND | 地 |
| 56 | ETH_TD2_P | 以太网 |
| 57 | GND | 地 |
| 58 | ETH_LED | 以太网 |
| 59 | GND | 地 |
| 60 | VDD_5V_IN | 电源 |
| 61 | VDD_5V_IN | 电源 |
| 62 | GND | 地 |
| 63 | RX_SBUS_INPUT_PORT | RC |
| 64 | SBUS_OUTPUT_PORT | RC |
| 65 | RSSI_IN_PORT | RC |
| 66 | PPM_IN_PORT | RC |
| 67 | VDD_5V_PERIPH_nEN | 电源控制 |
| 68 | VDD_5V_PERIPH_nOC | 电源控制 |
| 69 | VDD_5V_HIPOWER_nEN | 电源控制 |
| 70 | VDD_5V_HIPOWER_nOC | 电源控制 |
| 71 | NC | — |
| 72 | GND | 地 |
| 73 | SAFETY_SW | 安全开关 |
| 74 | SAFETY_SW_LED | 安全开关 |
| 75 | BUZZ- | 蜂鸣器 |
| 76 | GND | 地 |
| 77 | USB_D_P | USB |
| 78 | USB_D_N | USB |
| 79 | VBUS | USB |
| 80 | VBUS | USB |

### J2 — DF17(3.0)-80DS-0.5V(57)

| Pin | 网络名 | 类别 |
|-----|--------|------|
| 1 | SCK_EXT1 | SPI EXT1 |
| 2 | MISO_EXT1 | SPI EXT1 |
| 3 | MOSI_EXT1 | SPI EXT1 |
| 4 | CS2_EXT1 | SPI EXT1 |
| 5 | CS1_EXT1 | SPI EXT1 |
| 6 | nSYNC_EXT1 | SPI EXT1 |
| 7 | DRDY1_EXT1 | SPI EXT1 |
| 8 | DRDY2_EXT1 | SPI EXT1 |
| 9 | SPI_nRST | SPI EXT1 |
| 10 | ADC3_6V6_PORT | ADC |
| 11 | ADC3_3V3_PORT | ADC |
| 12 | nARMED_PORT | FMU |
| 13 | FMU_RST_REQ_PORT | FMU |
| 14 | FMU_BOOTLOADER_PORT | FMU |
| 15 | FMU_CAP1_PORT | FMU |
| 16 | nLED_BLUE | LED |
| 17 | nLED_GREEN | LED |
| 18 | nLED_RED | LED |
| 19 | GND | 地 |
| 20 | VDD_5V_IN | 电源 |
| 21 | VDD_5V_IN | 电源 |
| 22 | GND | 地 |
| 23 | NC | — |
| 24 | NC | — |
| 25 | NC | — |
| 26 | NC | — |
| 27 | NC | — |
| 28 | NC | — |
| 29 | NC | — |
| 30 | NC | — |
| 31 | NC | — |
| 32 | NC | — |
| 33 | GND | 地 |
| 34 | NC | — |
| 35 | NC | — |
| 36 | NC | — |
| 37 | NC | — |
| 38 | NC | — |
| 39 | NC | — |
| 40 | NC | — |
| 41 | IO-CH1-PORT | PWM/IO |
| 42 | IO-CH2-PORT | PWM/IO |
| 43 | IO-CH3-PORT | PWM/IO |
| 44 | IO-CH4-PORT | PWM/IO |
| 45 | IO-CH5-PORT | PWM/IO |
| 46 | IO-CH6-PORT | PWM/IO |
| 47 | IO-CH7-PORT | PWM/IO |
| 48 | IO-CH8-PORT | PWM/IO |
| 49 | GND | 地 |
| 50 | IO_nRST | IO |
| 51 | IO_SPARE_GPIO2 | GPIO |
| 52 | IO_SPARE_GPIO1 | GPIO |
| 53 | IO_SWCLK | SWD |
| 54 | IO_SWDIO | SWD |
| 55 | IO_SWO | SWD |
| 56 | IO_USART1_TX_DEBUG | 调试串口 |
| 57 | NC | — |
| 58 | VDD_SERVO_IN | 电源 |
| 59 | NC | — |
| 60 | VDD_5V_IN | 电源 |
| 61 | VDD_5V_IN | 电源 |
| 62 | NC | — |
| 63 | nPOWER_IN_A | 电源检测 |
| 64 | nPOWER_IN_B | 电源检测 |
| 65 | nPOWER_IN_C | 电源检测 |
| 66 | SDA_EXT2 | I2C EXT2 |
| 67 | SCL_EXT2 | I2C EXT2 |
| 68 | SDA_GPS1 | I2C GPS1 |
| 69 | SCL_GPS1 | I2C GPS1 |
| 70 | SDA_GPS2 | I2C GPS2 |
| 71 | SCL_GPS2 | I2C GPS2 |
| 72 | GND | 地 |
| 73 | NC | — |
| 74 | nIO_LED_BLUE | LED |
| 75 | nIO_LED_AMBER | LED |
| 76 | GND | 地 |
| 77 | CAN1_P | CAN |
| 78 | CAN1_N | CAN |
| 79 | CAN2_P | CAN |
| 80 | CAN2_N | CAN |

## EDA 操作步骤

1. 删除多余原理图页，仅保留一页并重命名为 Core_Carrier
2. 库中搜索 Hirose DF17 官方 footprint/symbol（80DP / 80DS）
3. 放置 J1=80DP @ +Y、J2=80DS @ −Y，载板侧 mirror=true
4. Pin1 位于连接器左上，与 carrier-pcb.dxf PIN1 标记对齐
5. NC 引脚加 No Connect；GND 引脚后续统一接 GND 符号（手动）
6. PCB 导入 carrier-pcb.dxf 后替换 DXF 参考焊盘为官方封装
