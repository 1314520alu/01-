# DF17(3.0)-80DS-0.5V(57) 引脚定义

| 项目 | 说明 |
|------|------|
| 座子型号 | DF17(3.0)-80DS-0.5V(57) |
| 引脚总数 | 80 |
| 编号约定 | **Core 底视**：左上=Pin1，左下=Pin80 · **载板原理图（rot180）**：右上=Pin1，左下=Pin80（右下=Pin79，见说明） |
| 上行 | Pin 1 → 40，自左向右 |
| 下行 | Pin 80 → 41，自左向右 |

> 飞控底部视图；载板侧连接器需镜像反向（见 [X9-Core 多旋翼底板接口设计说明](../X9-Core-多旋翼底板-接口设计说明.md)）。与 [80DP 座子](DF17-80DP-pinout.md) 配对使用。

---

## 完整引脚表（Pin 1–80）

| Pin | 信号名 | 类别 | Pin | 信号名 | 类别 |
|-----|--------|------|-----|--------|------|
| 1 | SCK_EXT1 | SPI EXT1 | 41 | IO-CH1-PORT | PWM/IO |
| 2 | MISO_EXT1 | SPI EXT1 | 42 | IO-CH2-PORT | PWM/IO |
| 3 | MOSI_EXT1 | SPI EXT1 | 43 | IO-CH3-PORT | PWM/IO |
| 4 | CS2_EXT1 | SPI EXT1 | 44 | IO-CH4-PORT | PWM/IO |
| 5 | CS1_EXT1 | SPI EXT1 | 45 | IO-CH5-PORT | PWM/IO |
| 6 | nSYNC_EXT1 | SPI EXT1 | 46 | IO-CH6-PORT | PWM/IO |
| 7 | DRDY1_EXT1 | SPI EXT1 | 47 | IO-CH7-PORT | PWM/IO |
| 8 | DRDY2_EXT1 | SPI EXT1 | 48 | IO-CH8-PORT | PWM/IO |
| 9 | SPI_nRST | SPI EXT1 | 49 | GND | 地 |
| 10 | ADC3_6V6_PORT | ADC | 50 | IO_nRST | IO |
| 11 | ADC3_3V3_PORT | ADC | 51 | IO_SPARE_GPIO2 | GPIO |
| 12 | nARMED_PORT | FMU | 52 | IO_SPARE_GPIO1 | GPIO |
| 13 | FMU_RST_REQ_PORT | FMU | 53 | IO_SWCLK | SWD |
| 14 | FMU_BOOTLOADER_PORT | FMU | 54 | IO_SWDIO | SWD |
| 15 | FMU_CAP1_PORT | FMU | 55 | IO_SWO | SWD |
| 16 | nLED_BLUE | LED | 56 | IO_USART1_TX_DEBUG | 调试串口 |
| 17 | nLED_GREEN | LED | 57 | NC | — |
| 18 | nLED_RED | LED | 58 | VDD_SERVO_IN | 电源 |
| 19 | GND | 地 | 59 | NC | — |
| 20 | VDD_5V_IN | 电源 | 60 | VDD_5V_IN | 电源 |
| 21 | VDD_5V_IN | 电源 | 61 | VDD_5V_IN | 电源 |
| 22 | GND | 地 | 62 | NC | — |
| 23 | NC | — | 63 | nPOWER_IN_A | 电源检测 |
| 24 | NC | — | 64 | nPOWER_IN_B | 电源检测 |
| 25 | NC | — | 65 | nPOWER_IN_C | 电源检测 |
| 26 | NC | — | 66 | SDA_EXT2 | I2C EXT2 |
| 27 | NC | — | 67 | SCL_EXT2 | I2C EXT2 |
| 28 | NC | — | 68 | SDA_GPS1 | I2C GPS1 |
| 29 | NC | — | 69 | SCL_GPS1 | I2C GPS1 |
| 30 | NC | — | 70 | SDA_GPS2 | I2C GPS2 |
| 31 | NC | — | 71 | SCL_GPS2 | I2C GPS2 |
| 32 | NC | — | 72 | GND | 地 |
| 33 | GND | 地 | 73 | NC | — |
| 34 | NC | — | 74 | nIO_LED_BLUE | LED |
| 35 | NC | — | 75 | nIO_LED_AMBER | LED |
| 36 | NC | — | 76 | GND | 地 |
| 37 | NC | — | 77 | CAN1_P | CAN |
| 38 | NC | — | 78 | CAN1_N | CAN |
| 39 | NC | — | 79 | CAN2_P | CAN |
| 40 | NC | — | 80 | CAN2_N | CAN |

---

## 按行排列（便于对照丝印）

### 上行 Pin 1–40（左 → 右）

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| SCK_EXT1 | MISO_EXT1 | MOSI_EXT1 | CS2_EXT1 | CS1_EXT1 | nSYNC_EXT1 | DRDY1_EXT1 | DRDY2_EXT1 | SPI_nRST | ADC3_6V6_PORT |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|----|----|----|----|----|----|----|----|----|-----|
| ADC3_3V3_PORT | nARMED_PORT | FMU_RST_REQ_PORT | FMU_BOOTLOADER_PORT | FMU_CAP1_PORT | nLED_BLUE | nLED_GREEN | nLED_RED | GND | VDD_5V_IN |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|----|----|----|----|----|----|----|----|----|-----|
| VDD_5V_IN | GND | NC | NC | NC | NC | NC | NC | NC | NC |

| 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|----|----|----|----|----|----|----|----|----|-----|
| NC | NC | GND | NC | NC | NC | NC | NC | NC | NC |

### 下行 Pin 80–41（左 = 80，右 = 41）

| 80 | 79 | 78 | 77 | 76 | 75 | 74 | 73 | 72 | 71 |
|----|----|----|----|----|----|----|----|----|-----|
| CAN2_N | CAN2_P | CAN1_N | CAN1_P | GND | nIO_LED_AMBER | nIO_LED_BLUE | NC | GND | SCL_GPS2 |

| 70 | 69 | 68 | 67 | 66 | 65 | 64 | 63 | 62 | 61 |
|----|----|----|----|----|----|----|----|----|-----|
| SDA_GPS2 | SCL_GPS1 | SDA_GPS1 | SCL_EXT2 | SDA_EXT2 | nPOWER_IN_C | nPOWER_IN_B | nPOWER_IN_A | NC | VDD_5V_IN |

| 60 | 59 | 58 | 57 | 56 | 55 | 54 | 53 | 52 | 51 |
|----|----|----|----|----|----|----|----|----|-----|
| VDD_5V_IN | NC | VDD_SERVO_IN | NC | IO_USART1_TX_DEBUG | IO_SWO | IO_SWDIO | IO_SWCLK | IO_SPARE_GPIO1 | IO_SPARE_GPIO2 |

| 50 | 49 | 48 | 47 | 46 | 45 | 44 | 43 | 42 | 41 |
|----|----|----|----|----|----|----|----|----|-----|
| IO_nRST | GND | IO-CH8-PORT | IO-CH7-PORT | IO-CH6-PORT | IO-CH5-PORT | IO-CH4-PORT | IO-CH3-PORT | IO-CH2-PORT | IO-CH1-PORT |

---

## 功能分组

### 电源

| Pin | 信号名 | 说明 |
|-----|--------|------|
| 20, 21, 60, 61 | VDD_5V_IN | 5 V 输入 |
| 58 | VDD_SERVO_IN | 舵机/外设 5 V 输入 |
| 63 | nPOWER_IN_A | 电源输入检测 A |
| 64 | nPOWER_IN_B | 电源输入检测 B |
| 65 | nPOWER_IN_C | 电源输入检测 C |

### 地（GND）

Pin：**19, 22, 33, 49, 72, 76**

### PWM / IO 通道

| Pin | 信号名 |
|-----|--------|
| 41 | IO-CH1-PORT |
| 42 | IO-CH2-PORT |
| 43 | IO-CH3-PORT |
| 44 | IO-CH4-PORT |
| 45 | IO-CH5-PORT |
| 46 | IO-CH6-PORT |
| 47 | IO-CH7-PORT |
| 48 | IO-CH8-PORT |

### CAN 总线

| Pin | 信号名 |
|-----|--------|
| 77 | CAN1_P |
| 78 | CAN1_N |
| 79 | CAN2_P |
| 80 | CAN2_N |

### I2C

| 总线 | SCL Pin | SDA Pin |
|------|---------|---------|
| GPS1 | 69 | 68 |
| GPS2 | 71 | 70 |
| EXT2 | 67 | 66 |

### SPI EXT1

| Pin | 信号名 |
|-----|--------|
| 1 | SCK_EXT1 |
| 2 | MISO_EXT1 |
| 3 | MOSI_EXT1 |
| 4 | CS2_EXT1 |
| 5 | CS1_EXT1 |
| 6 | nSYNC_EXT1 |
| 7 | DRDY1_EXT1 |
| 8 | DRDY2_EXT1 |
| 9 | SPI_nRST |

### SWD 调试（IO 侧）

| Pin | 信号名 |
|-----|--------|
| 53 | IO_SWCLK |
| 54 | IO_SWDIO |
| 55 | IO_SWO |
| 56 | IO_USART1_TX_DEBUG |

### FMU 控制 / 状态

| Pin | 信号名 |
|-----|--------|
| 10 | ADC3_6V6_PORT |
| 11 | ADC3_3V3_PORT |
| 12 | nARMED_PORT |
| 13 | FMU_RST_REQ_PORT |
| 14 | FMU_BOOTLOADER_PORT |
| 15 | FMU_CAP1_PORT |

### LED

| Pin | 信号名 | 说明 |
|-----|--------|------|
| 16 | nLED_BLUE | FMU 蓝灯 |
| 17 | nLED_GREEN | FMU 绿灯 |
| 18 | nLED_RED | FMU 红灯 |
| 74 | nIO_LED_BLUE | IO 蓝灯 |
| 75 | nIO_LED_AMBER | IO 琥珀灯 |

### GPIO / 复位

| Pin | 信号名 |
|-----|--------|
| 50 | IO_nRST |
| 51 | IO_SPARE_GPIO2 |
| 52 | IO_SPARE_GPIO1 |

### 未连接（NC）

Pin：**23–32, 34–40, 57, 59, 62, 73**

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-25 | 从零一 X9 Core DF17 引脚图提取，约定左上=1、左下=80 |
