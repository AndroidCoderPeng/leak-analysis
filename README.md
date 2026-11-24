# LeakAnalysis

漏水信号分析与相关定位桌面程序。项目使用 PySide6，不依赖 Qt Creator；`.ui` 对应的 Python 界面文件已随项目迁移，日常开发可直接在 PyCharm 中编辑 Python 文件。

## 在 PyCharm 中运行

1. 使用 PyCharm 打开本目录。
2. 在 **Settings → Project → Python Interpreter** 中选择项目解释器，建议使用本目录下的 `.venv`；若尚未创建，可在 PyCharm 中新建虚拟环境。
3. 在 PyCharm Terminal 安装依赖：

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. 将 `main.py` 配置为运行入口并启动。也可在 PyCharm 中直接打开 `main.py` 后运行。

命令行启动方式：

```powershell
python main.py
```

## 项目结构

- `main.py`：应用启动入口
- `MainWindow.py`、`ui_MainWindow.py`：主窗口逻辑及由 Qt Designer `.ui` 文件生成的界面代码
- `MainWindow.ui`：界面源文件；修改界面后需用 PySide6 的 `pyside6-uic` 更新 `ui_MainWindow.py`
- `data_analysis.py`：信号处理与定位算法
- `config/`、`data/`：配置及示例数据
