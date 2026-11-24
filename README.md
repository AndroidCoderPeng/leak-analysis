# LeakAnalysis

漏水信号分析与相关定位命令行工具。核心算法为纯 numpy/scipy 实现，不依赖任何界面框架；matplotlib 以 Agg 后端离屏渲染结果图片。

## 在 PyCharm 中运行

1. 使用 PyCharm 打开本目录。
2. 在 **Settings → Project → Python Interpreter** 中选择项目解释器，建议使用本目录下的 `.venv`；若尚未创建，可在 PyCharm
   中新建虚拟环境。
3. 在 PyCharm Terminal 安装依赖：

   ```powershell
   python -m pip install -r requirements.txt
   ```

## 使用方法

```powershell
# 最简用法：自动生成 report/ 目录（波形、频谱、相关曲线 PNG + result.json）
python cli.py data/测试数据.66.161317.txt -d 209 -v 1130

# 详细用法：自动生成 report/ 目录（波形、频谱、相关曲线 PNG + result.json）
python cli.py "data/测试数据.66.161317.txt" -c "data/参数配置.66.161317.json" --material 铸铁 --diameter 300

# 从 JSON 配置文件读取参数（命令行参数可覆盖配置文件）
python cli.py data/测试数据.66.161317.txt -c data/参数配置.66.161317.json

# 指定材料与管径，自动从 config/velocity_table.json 匹配声速
python cli.py data.txt -c cfg.json --material 铸铁 --diameter 200

# 只要结果不要图片
python cli.py data.txt -d 209 -v 1130 --no-plots
```

`python main.py` 等价于 `python cli.py`。

安装为命令行工具后可直接调用：

```powershell
python -m pip install -e .
leak-analysis data.txt -d 209 -v 1130
```

## 常用参数

| 参数                        | 说明                               | 默认值                       |
|-----------------------------|------------------------------------|------------------------------|
| `-c, --config`              | JSON 参数配置文件                  | 无                           |
| `-o, --output`              | 报告输出目录                       | `report`                     |
| `-d, --distance`            | 传感器间距 (m)                     | 配置文件或必填               |
| `-v, --velocity`            | 声速 (m/s)                         | 材料+管径自动匹配            |
| `--material` / `--diameter` | 管材名称 / 管径 (mm)，用于匹配声速 | 无                           |
| `--freq-min` / `--freq-max` | 频率范围 (Hz)                      | 0（不限）                    |
| `--sample-rate`             | 采样率 (Hz)                        | 7500                         |
| `--duration`                | 参与计算的信号时长 (s)             | 10                           |
| `--velocity-table`          | 管材声速表 JSON                    | `config/velocity_table.json` |
| `--no-plots`                | 不生成图片                         | -                            |

## 项目结构

- `cli.py`：命令行入口（`main.py` 为兼容入口）
- `core/analysis.py`：信号处理与相关定位算法（带通滤波、相关扫描、频谱）
- `core/io.py`：数据文件解析、JSON 配置加载、参数校验
- `core/materials.py`：管材声速表加载与匹配
- `report.py`：matplotlib Agg 后端，输出波形/频谱/相关曲线 PNG 与 `result.json`
- `config/velocity_table.json`：管材-管径-声速对照表
- `data/`：示例数据与配置
- `report/`：运行后的输出目录（自动创建）

## 数据文件格式

文本文件，每行一个数值，支持：

- 首行为时间戳/表头，数值数据用 `====` 分隔行区分 A、B 通道；
- 无分隔行时，纯数值数据前后对半分为 A、B 两个通道。

## 配置文件格式

JSON 对象，字段名与旧界面版配置完全兼容：

```json
{
  "PipeMaterial": "铸铁",
  "PipeDiameter": "200",
  "PipeLength": "209",
  "MinFrequency": "100",
  "MaxFrequency": "3000"
}
```
