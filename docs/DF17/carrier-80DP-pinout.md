# 载板 DF17(1.0H)-80DP-0.5V(57) 引脚定义

| 项目 | 说明 |
|------|------|
| 角色 | **载板** |
| 座子型号 | DF17(1.0H)-80DP-0.5V(57) |
| 引脚总数 | 80 |
| 载板位置 | PCB **+Y** |
| 对接 Core | **80DS** |
| 网络来源 | 同 Pin 号取自 [Core 80DS](DF17-80DS-pinout.md) |
| 编号约定 | 上排奇数 Pin1,3,…,79（左→右）；下排偶数 Pin2,4,…,80（左→右） |
| 载板 Top View | Pin1 **右上** · Pin2 **右下** · Pin79 **左上** · Pin80 **左下**（相对 Core 底视左右 180° 镜像） |

> 载板原理图/PCB 标网用本表。Core 侧定义见 [80DS](DF17-80DS-pinout.md)。

---

## 完整引脚表（Pin 1–80）

| Pin | 信号名 | 类别 | Pin | 信号名 | 类别 |
|-----|--------|------|-----|--------|------|
| 1 | SCK_EXT1 | SPI EXT1 | 2 | CAN2_N | CAN |
| 3 | MISO_EXT1 | SPI EXT1 | 4 | CAN2_P | CAN |
| 5 | MOSI_EXT1 | SPI EXT1 | 6 | CAN1_N | CAN |
| 7 | CS2_EXT1 | SPI EXT1 | 8 | CAN1_P | CAN |
| 9 | CS1_EXT1 | SPI EXT1 | 10 | GND | 地 |
| 11 | nSYNC_EXT1 | SPI EXT1 | 12 | nIO_LED_AMBER | LED |
| 13 | DRDY1_EXT1 | SPI EXT1 | 14 | nIO_LED_BLUE | LED |
| 15 | DRDY2_EXT1 | SPI EXT1 | 16 | NC | — |
| 17 | SPI_nRST | SPI EXT1 | 18 | GND | 地 |
| 19 | ADC3_6V6_PORT | ADC | 20 | SCL_GPS2 | I2C GPS2 |
| 21 | ADC3_3V3_PORT | ADC | 22 | SDA_GPS2 | I2C GPS2 |
| 23 | nARMED_PORT | FMU | 24 | SCL_GPS1 | I2C GPS1 |
| 25 | FMU_RST_REQ_PORT | FMU | 26 | SDA_GPS1 | I2C GPS1 |
| 27 | FMU_BOOTLOADER_PORT | FMU | 28 | SCL_EXT2 | I2C EXT2 |
| 29 | FMU_CAP1_PORT | FMU | 30 | SDA_EXT2 | I2C EXT2 |
| 31 | nLED_BLUE | LED | 32 | nPOWER_IN_C | 电源检测 |
| 33 | nLED_GREEN | LED | 34 | nPOWER_IN_B | 电源检测 |
| 35 | nLED_RED | LED | 36 | nPOWER_IN_A | 电源检测 |
| 37 | GND | 地 | 38 | NC | — |
| 39 | VDD_5V_IN | 电源 | 40 | VDD_5V_IN | 电源 |
| 41 | VDD_5V_IN | 电源 | 42 | VDD_5V_IN | 电源 |
| 43 | GND | 地 | 44 | NC | — |
| 45 | NC | — | 46 | VDD_SERVO_IN | 电源 |
| 47 | NC | — | 48 | NC | — |
| 49 | NC | — | 50 | IO_USART1_TX_DEBUG | 调试串口 |
| 51 | NC | — | 52 | IO_SWO | SWD |
| 53 | NC | — | 54 | IO_SWDIO | SWD |
| 55 | NC | — | 56 | IO_SWCLK | SWD |
| 57 | NC | — | 58 | IO_SPARE_GPIO1 | GPIO |
| 59 | NC | — | 60 | IO_SPARE_GPIO2 | GPIO |
| 61 | NC | — | 62 | IO_nRST | IO |
| 63 | NC | — | 64 | GND | 地 |
| 65 | GND | 地 | 66 | IO-CH8-PORT | PWM/IO |
| 67 | NC | — | 68 | IO-CH7-PORT | PWM/IO |
| 69 | NC | — | 70 | IO-CH6-PORT | PWM/IO |
| 71 | NC | — | 72 | IO-CH5-PORT | PWM/IO |
| 73 | NC | — | 74 | IO-CH4-PORT | PWM/IO |
| 75 | NC | — | 76 | IO-CH3-PORT | PWM/IO |
| 77 | NC | — | 78 | IO-CH2-PORT | PWM/IO |
| 79 | NC | — | 80 | IO-CH1-PORT | PWM/IO |

---

## 按行排列（便于对照丝印）

### 上排奇数 Pin 1,3,…,79（左 → 右）

| 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 |
|---|---|---|---|---|---|---|---|---|---|
| SCK_EXT1 | MISO_EXT1 | MOSI_EXT1 | CS2_EXT1 | CS1_EXT1 | nSYNC_EXT1 | DRDY1_EXT1 | DRDY2_EXT1 | SPI_nRST | ADC3_6V6_PORT |

| 21 | 23 | 25 | 27 | 29 | 31 | 33 | 35 | 37 | 39 |
|---|---|---|---|---|---|---|---|---|---|
| ADC3_3V3_PORT | nARMED_PORT | FMU_RST_REQ_PORT | FMU_BOOTLOADER_PORT | FMU_CAP1_PORT | nLED_BLUE | nLED_GREEN | nLED_RED | GND | VDD_5V_IN |

| 41 | 43 | 45 | 47 | 49 | 51 | 53 | 55 | 57 | 59 |
|---|---|---|---|---|---|---|---|---|---|
| VDD_5V_IN | GND | NC | NC | NC | NC | NC | NC | NC | NC |

| 61 | 63 | 65 | 67 | 69 | 71 | 73 | 75 | 77 | 79 |
|---|---|---|---|---|---|---|---|---|---|
| NC | NC | GND | NC | NC | NC | NC | NC | NC | NC |

### 下排偶数 Pin 80,78,…,2（左 = 80，右 = 2）

| 80 | 78 | 76 | 74 | 72 | 70 | 68 | 66 | 64 | 62 |
|---|---|---|---|---|---|---|---|---|---|
| IO-CH1-PORT | IO-CH2-PORT | IO-CH3-PORT | IO-CH4-PORT | IO-CH5-PORT | IO-CH6-PORT | IO-CH7-PORT | IO-CH8-PORT | GND | IO_nRST |

| 60 | 58 | 56 | 54 | 52 | 50 | 48 | 46 | 44 | 42 |
|---|---|---|---|---|---|---|---|---|---|
| IO_SPARE_GPIO2 | IO_SPARE_GPIO1 | IO_SWCLK | IO_SWDIO | IO_SWO | IO_USART1_TX_DEBUG | NC | VDD_SERVO_IN | NC | VDD_5V_IN |

| 40 | 38 | 36 | 34 | 32 | 30 | 28 | 26 | 24 | 22 |
|---|---|---|---|---|---|---|---|---|---|
| VDD_5V_IN | NC | nPOWER_IN_A | nPOWER_IN_B | nPOWER_IN_C | SDA_EXT2 | SCL_EXT2 | SDA_GPS1 | SCL_GPS1 | SDA_GPS2 |

| 20 | 18 | 16 | 14 | 12 | 10 | 8 | 6 | 4 | 2 |
|---|---|---|---|---|---|---|---|---|---|
| SCL_GPS2 | GND | NC | nIO_LED_BLUE | nIO_LED_AMBER | GND | CAN1_P | CAN1_N | CAN2_P | CAN2_N |

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-25 | 由 Core 引脚表交叉映射生成（载板 DS←Core DP，载板 DP←Core DS） |
