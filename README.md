# 01飞控 — X9 Core 多旋翼底板

为零一飞行 [X9 Core](https://docs.01aero.cn/docs/JfRLkT8E) 设计多旋翼载板（EasyEDA）。

## 文档

| 文件 | 说明 |
|------|------|
| [docs/X9-Core-多旋翼底板-接口设计说明.md](docs/X9-Core-多旋翼底板-接口设计说明.md) | 接口需求、电源架构、串口映射、PWM/CAN 分配 |
| [docs/DF17/](docs/DF17/) | 两颗 DF17 80pin 引脚定义（[80DS](docs/DF17/DF17-80DS-pinout.md) / [80DP](docs/DF17/DF17-80DP-pinout.md)） |
| [db/pinout.db](db/pinout.db) | SQLite 引脚库（`python tools/import_df17_pinout.py` 同步） |
| [docs/DF17/cad/](docs/DF17/cad/) | X9 Core 底面 DXF 机械图 |

## 下一步

1. 向零一飞行索取 **DF17 封装尺寸 DXF**（pinout 已录入 [docs/DF17/](docs/DF17/)）
2. 在 EasyEDA 按设计说明第 9 节分区绘制原理图
3. 载板原理图网络名与 [80DS](docs/DF17/DF17-80DS-pinout.md)、[80DP](docs/DF17/DF17-80DP-pinout.md) pinout 核对

## 固件

- 机型：**ArduCopter**
- 固件：[零一 X9 ArduPilot 资源](https://pan.01aero.cn/s/mYhv零一飞行资源库/X9系列飞控/ArduPilot固件)
