# X9 Core 多旋翼飞控底板 — 接口需求与引脚分配

> 适配文档：[零一飞行 X9 系列飞控说明书](https://docs.01aero.cn/docs/JfRLkT8E)  
> 目标机型：多旋翼（ArduCopter）  
> EDA 工具：嘉立创 EasyEDA  
> 文档版本：v0.1 · 2026-06-25

---

## 1. 设计目标

为 **X9 Core**（无自带接口板）设计一块多旋翼载板，实现：

1. 通过底部 **DF17** 连接器与 X9 Core 可靠对接（机械 + 电气）
2. 复用 X9 Cube 接口板的 **连接器型号与线序习惯**，降低线束与调试成本
3. 满足典型多旋翼外设：电源、GPS、数传、遥控、CAN 设备、PWM 电调
4. 工作电压 **4.5 V–5.4 V**（飞控供电），外设 5 V 由载板电源切换模块分配

### 1.1 X9 Core 关键参数（摘自官方文档）

| 项目 | 规格 |
|------|------|
| 主 MCU | STM32H753 |
| IO MCU | STM32F103 |
| IMU | IIM42652 ×3（三余度） |
| 气压计 | ICP-20100×2 或 BMP581+SPL07 |
| 磁罗盘 | RM3100（内置） |
| 工作电压 | 4.5 V–5.4 V |
| 尺寸 | 38.8 × 38.8 × 26.5 mm |
| 重量 | 72 g |
| PWM 能力 | 14 路（经 DF17 引出） |
| 机型 | 直升机、多旋翼、固定翼、VTOL、车、船 |

---

## 2. 机械与连接器

### 2.1 DF17 对接（载板侧）

- 官方说明：文档中 **DF17 引脚图、尺寸图为飞控底部视图**；设计载板时 **连接器方向与丝印需镜像反向**。
- 载板应预留：
  - DF17 母座（或按零一提供的推荐料号选型）
  - X9 Core 安装高度与减震/支撑结构（参考 Cube 系列载板做法：四角支撑 + 中央 DF17）
  - 散热与 IMU 减震：Core 内置减震，载板 **不得** 对飞控本体施加额外刚性约束

> **Pinout 已录入**：[80DS](DF17/DF17-80DS-pinout.md)、[80DP](DF17/DF17-80DP-pinout.md)。**待补充**：封装尺寸图 DXF（购买 X9 Core 用户可向厂商索取底板设计资源）。

### 2.2 对外连接器型号（与 X9 Cube 一致）

| 接口 | 连接器型号 | 针数 | 载板角色 |
|------|------------|------|----------|
| POWER1 / POWER2 | Molex 5055650601 | 6 | 电源输入（接 OnePMU 或等效 CAN 电源模块） |
| TELEM1 / TELEM2 / GPS1 / GPS2 / CAN1 / CAN2 / SBUS / I2C / ETH / AUX 等 | JST-GH 1.25 mm | 4 | 信号与外设 |
| USB | Type-C 或 GH 扩展 | — | 地面站配置 / 刷固件 |

---

## 3. 电源架构

### 3.1 电源切换模块（载板必须实现）

官方提供电源切换模块参考设计，载板需实现 **双路 Brick 输入 + USB + 外设配电**：

| 模块信号序号 | 信号名 | 载板连接 |
|-------------|--------|----------|
| 1–3 | nPOWER_IN_A/B/C | → X9 Core 同名脚（电源选择逻辑） |
| 4–5 | VBUS | ← USB Type-C |
| 6–7 | VDD_5V_BRICK2 | ← POWER2（Molex 6pin） |
| 8–9 | VDD_5V_BRICK1 | ← POWER1（Molex 6pin） |
| 10 | VDD_5V_IN | → X9 Core 系统 5 V 输入 |
| 11 | VDD_5V_HIPOWER | → 高耗电外设接口（如部分舵机总线，多旋翼可预留） |
| 12 | VDD_5V_PERIPH | → 普通外设 5 V（GPS、数传、接收机等） |
| 13 | FMU_VDD_3V3 | 飞控上拉参考 |
| 14–15 | GND | 地 |
| 16 | VDD_5V_PERIPH_nEN | ↔ X9 Core 外设电源使能 |
| 17 | VDD_5V_PERIPH_nOC | ↔ X9 Core 外设过流反馈 |
| 18 | VDD_5V_HIPOWER_nEN | ↔ X9 Core 高耗使能 |
| 19 | VDD_5V_HIPOWER_nOC | ↔ X9 Core 高耗过流反馈 |

### 3.2 多旋翼电源设计建议

| 路径 | 建议 |
|------|------|
| 主供电 | POWER1 接 **OnePMU / DroneCAN 电源模块**（推荐），POWER2 作冗余或第二电池监测 |
| 飞控供电 | 经切换模块输出 **VDD_5V_IN**，保证 4.5–5.4 V |
| 外设 5 V | GPS、数传、接收机走 **VDD_5V_PERIPH**，总电流按器件手册核算 |
| 电调供电 | **大电流动力电不经过载板 5 V 轨**；PWM 仅信号，ESC BEC 或独立 UBEC 供舵机/外设时注意共地 |
| USB | 地面调试时 VBUS 参与供电切换，原理图按官方参考实现防反灌 |

---

## 4. 串口映射（ArduPilot SERIAL 约定）

载板丝印与参数配置须与下表一致（摘自官方文档）：

| SERIAL | 载板丝印 | MCU UART | DMA | 多旋翼典型用途 |
|--------|----------|----------|-----|----------------|
| SERIAL0 | USB | OTG1 | — | 地面站 / 刷固件 |
| SERIAL1 | TELEM1 | UART7 | 已启用 | 数传（OneDLink / OneVDLink / 三方） |
| SERIAL2 | TELEM2 | UART5 | 已启用 | 备用数传 / 伴飞计算机 |
| SERIAL3 | GPS1 | USART1 | 已启用 | 主 GPS（建议接含安全开关/蜂鸣器/LED 的 GPS 座） |
| SERIAL4 | GPS2 | UART8 | 已启用 | 副 GPS / RTK 漫游 |
| SERIAL5 | TELEM3 | USART2 | 已启用 | RS232 数传或 MAVLink 设备 |
| SERIAL6 | UART4 | UART4 | 已启用 | 扩展串口（测距、4G 等） |
| SERIAL7 | DEBUG | USART3 | 已启用 | 调试（生产可不外接） |
| SERIAL8 | SLCAN | USB OTG | — | CAN 调试（通常不占用载板座子） |

### 4.1 JST-GH 4pin 串口线序（与 Pixhawk 系习惯对齐）

载板对外座子建议统一：

```text
Pin1  VCC  (5 V，来自 VDD_5V_PERIPH，经座子侧可选串阻/保险)
Pin2  TX   (飞控 → 外设 RX)
Pin3  RX   (飞控 ← 外设 TX)
Pin4  GND
```

TELEM3（USART2）若接 RS232 设备，载板侧应放 **TTL↔RS232 电平转换** 或单独 RS232 座子，勿与 TTL 座子混用。

---

## 5. 多旋翼接口功能分配

### 5.1 载板对外接口清单（推荐）

| 序号 | 载板接口 | 数量 | 优先级 | 说明 |
|------|----------|------|--------|------|
| P1 | POWER1 | 1 | 必须 | 主电源 + CAN PMU |
| P2 | POWER2 | 1 | 推荐 | 冗余电源监测 |
| P3 | GPS1 | 1 | 必须 | 主定位；建议兼容零一 GPS&Safety 线序 |
| P4 | TELEM1 | 1 | 必须 | 主数传 |
| P5 | SBUS IN | 1 | 必须 | 遥控接收机（或预留 CRSF 需确认硬件支持） |
| P6 | CAN1 | 1 | 推荐 | DroneCAN ESC / 罗盘 / 气压计 |
| P7 | CAN2 | 1 | 可选 | 第二 CAN 总线 |
| P8 | M1–M8 | 8 | 按机型 | 四轴用 4 路，六轴 6 路，八轴 8 路 |
| P9 | M9–M14 | 6 | 可选 | 扩展电机或 AUX PWM |
| P10 | TELEM2 | 1 | 可选 | 第二数传 |
| P11 | GPS2 | 1 | 可选 | 双 GPS / RTK |
| P12 | I2C | 1 | 可选 | 外置传感器 |
| P13 | USB Type-C | 1 | 必须 | 调参刷机 |
| P14 | ETH | 1 | 可选 | 网口相机 / 伴飞 |
| P15 | AD&IO | 1 | 可选 | 模拟电流计 / Bootloader |
| P16 | DSM/PPM IN | 1 | 可选 | 替代 SBUS 的接收机协议 |

X9 最多 **14 路 PWM**；四旋翼占用 M1–M4，六旋翼 M1–M6，八旋翼 M1–M8，余量可作蜂鸣器、相机快门等 AUX。

### 5.2 电机 PWM 通道与 ArduCopter 映射

ArduCopter 默认电机顺序与 **物理安装位置** 相关，载板丝印 **M1–Mn 应一一对应飞控 PWM 输出编号**（经 DF17 映射后的逻辑通道），地面站 Motor Test 逐路验证。

**四旋翼（Quad X）推荐丝印与功能：**

| 载板丝印 | ArduCopter 电机号 | 典型位置 | 备注 |
|----------|-------------------|----------|------|
| M1 | Motor 1 | 右前 | 方向以桨叶实测为准 |
| M2 | Motor 2 | 左后 | |
| M3 | Motor 3 | 左前 | |
| M4 | Motor 4 | 右后 | |
| M5–M8 | AUX / 未用 | — | 预留 |

**六旋翼 / 八旋翼**：按 `FRAME_CLASS` 扩展 M1–M6 或 M1–M8；下载固件时选择 **ArduCopter**，机架类型在地面站配置。

### 5.3 PWM 电气特性

- 官方说明（X6 同系列）：**M1–M14 支持 DShot**（部分高端通道支持双向 DShot，以 X9 固件与 hwdef 为准）。
- 载板 PWM 走线：
  - 信号线短、等长优先；远离电源与大电流回路
  - 每路飞控侧近端可选 **33 Ω–100 Ω** 串联阻尼
  - 电调信号地与电源地 **单点共地** 于载板电源入口

---

## 6. CAN 总线

| 项目 | 建议 |
|------|------|
| 拓扑 | CAN1 为主总线，终端电阻 **120 Ω** 在总线两端各一（载板可在 CAN1 座子旁跳线选择是否内置终端） |
| 用途 | DroneCAN 电调、OnePMU、OneASP 空速计、OneRTK 等 |
| 线序 | 遵循 DroneCAN：CAN_H、CAN_L、GND、5 V（按零一线材定义） |
| 速率 | 默认 1 Mbps；长缆/多节点按 ArduPilot 文档降速测试 |

---

## 7. 遥控与 GPS

### 7.1 SBUS IN

- 接 4pin GH：信号 + 5 V + GND（接收机供电从 VDD_5V_PERIPH）
- 注意 SBUS 为 **反相串口**，飞控硬件已处理；载板勿再反相

### 7.2 GPS1（推荐集成座）

多旋翼强烈建议使用带 **安全开关、蜂鸣器、RGB LED** 的 GPS 座，便于解锁逻辑与状态指示。线序对齐零一 **GPS&Safety** 或 Pixhawk 兼容座。

### 7.3 内置罗盘

X9 Core 已内置 **RM3100**，外接 GPS 罗盘模块时须在地面站设置 `COMPASS_USE` / `COMPASS_PRIO` 避免冲突；载板无额外动作，调试文档中说明即可。

---

## 8. 固件与调试检查单

| 步骤 | 内容 |
|------|------|
| 1 | 刷入零一提供的 **X9 系列 ArduCopter** 固件（[资源库](https://pan.01aero.cn/s/mYhv零一飞行资源库/X9系列飞控/ArduPilot固件)） |
| 2 | Mission Planner / QGC：加速度计、罗盘、遥控、ESC 校准 |
| 3 | 确认 `SERIAL1_PROTOCOL` 等数传参数与 TELEM1 一致 |
| 4 | Motor Test：M1–M4 与桨叶位置、转向一致 |
| 5 | DroneCAN：若用 CAN 电调，确认 `CAN_D1_PROTOCOL=1` 及节点发现 |
| 6 | 解锁前：GPS 定位、罗盘健康、电源监测（Battery Monitor）正常 |

---

## 9. EasyEDA 原理图分区建议

便于后续画原理图，建议工程按 **Sheet** 划分：

```text
01_Power_Switching     电源切换 + POWER1/2 + USB-C
02_DF17_Interface      DF17 插座及至各子系统的网络标签
03_PWM_Outputs         M1–M14 输出 + GH 座子
04_Telemetry_GPS       TELEM1/2/3, GPS1/2
05_CAN_Bus             CAN1/2 + 终端电阻跳线
06_RC_SBUS             SBUS / DSM-PPM
07_Misc                I2C, ETH, AD&IO, SPI, LED/按键
08_Mechanical          板框、安装孔、DF17 定位（导入官方 DXF 后补）
```

### 9.1 设计规则（DRA）

| 项目 | 建议 |
|------|------|
| 板层 | 4 层：Top 信号 / GND / PWR / Bottom 信号 |
| 线宽 | 5 V 主供电 ≥ 0.5 mm（按电流核算）；PWM ≥ 0.2 mm |
| 过孔 | 电源地密集过孔围栏 |
| 丝印 | 每个 GH 座标注：接口名 + Pin1 方向 + SERIAL 号 |

---

## 10. 待办与风险

| 项 | 状态 | 说明 |
|----|------|------|
| DF17 完整 80pin 定义 | 已完成 | 见 [80DS](DF17/DF17-80DS-pinout.md)、[80DP](DF17/DF17-80DP-pinout.md)；封装 DXF 仍待索取 |
| 电源切换原理图 | 待画 | 严格对照官方「电源切换模块」原理图 |
| TELEM3 RS232 电平 | 待确认 | 是否板载 MAX3232 或仅 TTL |
| DShot 双向 | 待确认 | 以 X9 hwdef 为准，影响 M 通道布局 |
| 板厚与结构 | 待确认 | 与机身安装空间、减震方案联调 |

---

## 11. 参考链接

- [X9 系列飞控说明书](https://docs.01aero.cn/docs/JfRLkT8E)
- [ArduPilot 固件（零一盘）](https://pan.01aero.cn/s/mYhv零一飞行资源库/X9系列飞控/ArduPilot固件)
- [Mission Planner](https://firmware.ardupilot.org/Tools/MissionPlanner)
- [QGroundControl](https://github.com/mavlink/qgroundcontrol/releases)

---

## 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.1 | 2026-06-25 | 初版：多旋翼接口需求与引脚分配 |
