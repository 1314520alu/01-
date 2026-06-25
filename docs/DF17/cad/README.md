# X9 Core 底面 CAD

根据官方底面机械图生成的可编辑 CAD 文件，用于 EasyEDA / Altium / FreeCAD 等导入参考。

## 文件

| 文件 | 说明 |
|------|------|
| [X9-Core-bottom.dxf](X9-Core-bottom.dxf) | Core 底面机械参考（Bottom View） |
| [carrier-pcb.dxf](carrier-pcb.dxf) | **载板 PCB 用**（Top View，可直接导入 EasyEDA） |
| [X9-Core-bottom-reference.png](X9-Core-bottom-reference.png) | 官方底面机械图扫描/截图 |

## 生成

```bash
pip install ezdxf
python tools/generate_x9_bottom_cad.py      # Core 底面机械
python tools/generate_carrier_pcb_dxf.py    # 载板 PCB
```

## 图层

| 图层 | 内容 |
|------|------|
| `OUTLINE` | 外形 38.80×38.80（R3 圆角） |
| `MOUNT_HOLES` | 四角安装孔 φ2.10 通孔 |
| `MOUNT_CB` | 沉孔 φ3.60×0.65 |
| `CONNECTOR` | 两颗 DF17 壳体投影 4×24 mm |
| `DF17_PADS` | 80pin 0.5mm pitch 焊盘参考 |
| `CENTER_RIBS` | 中央加强筋示意 |
| `M2_HOLES` | 3×φ1.60 / M2-6H |
| `PIN1_MARK` | Pin1 位置标记 |
| `DIM` / `TEXT` | 尺寸与说明 |

## 关键尺寸（mm）

| 项目 | 值 |
|------|-----|
| 外形 | 38.80 × 38.80 |
| 安装孔距 | 32 × 32（中心 ±16） |
| 安装孔 | φ2.10 通孔，沉孔 φ3.60↓0.65 |
| 连接器中心 | X = ±16 |
| 连接器投影 | 4 × 24 |
| 中央筋位宽度 | 14 |
| M2 孔 | 3×φ1.60↓3 |

**坐标原点：** 几何中心 `(0, 0)`  
**视图：** 底面（Bottom View），沿 −Z 看向 Core 底面

---

## carrier-pcb.dxf（载板 PCB）

| 项目 | 说明 |
|------|-----|
| 视图 | **载板 Top View**（PCB 设计视角，已按 mating 配对 DS/DP） |
| 板框 | 80 × 80 mm（可导入后改大） |
| Core 占位 | 38.80 虚线框 |
| 安装孔 | 32 × 32，φ2.50（M2 螺丝） |
| 上侧 (+Y) | **80DP**（对接 Core 80DS） |
| 下侧 (−Y) | **80DS**（对接 Core 80DP） |
| Pin1 | 每颗连接器 **左上**，与 pinout 约定一致 |

### EasyEDA 导入

1. PCB 编辑器 → **文件 → 导入 → DXF**
2. 图层映射：`BOARD_OUTLINE` → 板框；`DRILL`/`HOLE` → 钻孔；`PAD`/`FOOTPRINT` → 参考
3. **焊盘请换用 Hirose 官方 footprint**，DXF 中 PAD 仅为对齐参考
4. 以 **PIN1** 标记与官方封装 Pin1 重合为验收标准

## 注意事项（Core 底面 DXF）

1. **M2 孔 Y 坐标**（±6 mm）为按底图比例估算，正式开模/开板前请与零一官方 DXF 复核。
2. **DF17 焊盘**按 Hirose 0.5 mm pitch、80pin 双列生成，仅为参考；载板应使用官方 DS/DP footprint。
3. 布局示意图（[connector-layout](../images/X9-Core-DF17-connector-layout.png)）为 **上 80DS / 下 80DP** 示意；本机械图为 **左 / 右** 两颗连接器投影，设计时以本 DXF 尺寸为准并镜像到载板。
