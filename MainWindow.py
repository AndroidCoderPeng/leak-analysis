# This Python file uses the following encoding: utf-8
import json
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from data_analysis import locate, spectrum
from ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._correlation_figure = Figure(figsize=(7, 2.4), tight_layout=True)
        self._correlation_canvas = FigureCanvasQTAgg(self._correlation_figure)
        self._correlation_canvas.setMinimumHeight(190)
        self.ui.corrPlotLayout.setContentsMargins(2, 2, 2, 2)
        self.ui.corrPlotLayout.addWidget(self._correlation_canvas)
        self._correlation_canvas.hide()
        self._wave_a_figure, self._wave_a_canvas, self._wave_a_axes = (
            self._create_signal_plot(self.ui.waveBoxA, 1.15)
        )
        self._wave_b_figure, self._wave_b_canvas, self._wave_b_axes = (
            self._create_signal_plot(self.ui.waveBoxB, 1.15)
        )
        self._spectrum_figure, self._spectrum_canvas, self._spectrum_axes = (
            self._create_signal_plot(self.ui.specBox, 2.2)
        )

        self._data_a = []
        self._data_b = []
        self._bands = [(100, 300), (200, 500), (400, 800),
                       (600, 1200), (800, 1600), (1000, 2000),
                       (1200, 3000)]
        self._data_file = ""
        self._config_file = ""

        self.ui.btnImportData.clicked.connect(self.import_data)
        self.ui.btnImportCfg.clicked.connect(self.import_config)
        self.ui.btnRun.clicked.connect(self.calculate)
        self.ui.cfgMaterial.currentIndexChanged.connect(self.match_velocity)
        self.ui.cfgDiam.valueChanged.connect(self.match_velocity)

        self._velocity_entries = self._default_velocity_entries()
        self._refresh_materials()

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入数据文件",
            "",
            "数据文件 (*.txt *.dat);;所有文件 (*)",
        )
        if not file_path:
            return

        try:
            data_a, data_b = self._parse_data_file(file_path)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, "导入失败", str(exc))
            return

        self._data_a = data_a
        self._data_b = data_b
        self._data_file = file_path

        self.ui.fileNameLabel.setText(Path(file_path).name)
        self.ui.stLen.setText(f"{len(data_a)}")
        self.ui.stAamp.setText(self._amplitude_range(data_a))
        self.ui.stBamp.setText(self._amplitude_range(data_b))
        self._draw_signal_previews()

        duration = len(data_a) / 7500.0
        if duration < 10:
            self.ui.sigDur.setText(f"共 {duration:.1f} s（采样率 7500Hz）")
        else:
            self.ui.sigDur.setText("前 10 s（采样率 7500Hz）")

        self.statusBar().showMessage(f"已导入数据：{file_path}", 5000)

    def import_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入配置文件",
            "",
            "配置文件 (*.json);;所有文件 (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                config = json.load(file)
            if not isinstance(config, dict):
                raise ValueError("配置文件根节点必须为 JSON 对象")

            applied = self._apply_config(config)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            QMessageBox.warning(self, "导入失败", f"无法导入配置：{exc}")
            return

        if applied == 0:
            QMessageBox.warning(self, "导入失败", "配置文件中未找到任何可识别字段")
            return

        self._config_file = file_path
        self.statusBar().showMessage(
            f"已导入配置：{Path(file_path).name}（{applied} 项）", 5000
        )

    def calculate(self):
        problems = []
        if not self._data_a or not self._data_b:
            problems.append("尚未导入数据文件")
        elif len(self._data_a) != len(self._data_b):
            problems.append(
                f"A/B 通道数据长度不一致（A: {len(self._data_a)}，B: {len(self._data_b)}）"
            )

        distance = float(self.ui.cfgDis.value())
        velocity = float(self.ui.cfgVelo.value())
        freq_min = float(self.ui.cfgFreqMin.value())
        freq_max = float(self.ui.cfgFreqMax.value())

        if distance <= 0:
            problems.append("传感器距离必须大于 0")
        if freq_min > freq_max:
            problems.append("最小频率不能大于最大频率")
        if velocity <= 0:
            problems.append("声速必须大于 0")
        elif velocity < 100 or velocity > 6000:
            problems.append("声速超出合理范围（100 ~ 6000 m/s）")

        if problems:
            QMessageBox.warning(self, "参数校验未通过", "\n".join(problems))
            return

        bands = self._bands or [(freq_min, freq_max)]
        if freq_min > 0 or freq_max > 0:
            bands = [band for band in bands
                     if band[0] >= freq_min and band[1] <= freq_max]
        if not bands:
            bands = [(freq_min, freq_max)]

        try:
            result = locate(
                self._data_a[:min(10 * 7500, len(self._data_a))],
                self._data_b[:min(10 * 7500, len(self._data_b))],
                distance,
                velocity,
                bands,
            )
        except Exception as exc:
            QMessageBox.warning(self, "定位失败", str(exc))
            return

        if not result.ok:
            QMessageBox.warning(self, "定位失败", "没有有效频段参与计算，请检查参数和频段范围")
            return

        self.ui.mDisA.setText(f"{result.dis_a:.2f}")
        self.ui.mDisB.setText(f"{result.dis_b:.2f}")
        self.ui.mSnr.setText(f"{result.snr:.2f}")
        self.ui.corrEmpty.setVisible(False)
        self.ui.correlationSubtitle.setText(
            f"最优频段 {result.best_low}-{result.best_high} Hz · "
            f"扫描 {result.bands_used} 档 · 峰值相关系数 {result.coefficient:.4f}"
        )
        self._draw_localization_result(result, distance)

        self.statusBar().showMessage(
            f"定位完成：最优频段 {result.best_low}-{result.best_high} Hz，"
            f"SNR={result.snr:.2f}",
            8000,
        )

    def _create_signal_plot(self, container, height):
        figure = Figure(figsize=(7, height), tight_layout=True)
        canvas = FigureCanvasQTAgg(figure)
        canvas.setMinimumHeight(90)
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().addWidget(canvas)
        axes = figure.subplots()
        return figure, canvas, axes

    def _draw_signal_previews(self):
        sample_rate = 7500.0
        preview_length = min(10 * int(sample_rate), len(self._data_a), len(self._data_b))
        sample_indices = range(preview_length)
        time_axis = [index / sample_rate for index in sample_indices]

        self._draw_signal_axis(
            self._wave_a_figure, self._wave_a_canvas, self._wave_a_axes,
            time_axis, self._data_a[:preview_length], "时间 (s)", "A 通道幅值",
            "#2563eb",
        )
        self._draw_signal_axis(
            self._wave_b_figure, self._wave_b_canvas, self._wave_b_axes,
            time_axis, self._data_b[:preview_length], "时间 (s)", "B 通道幅值",
            "#f97316",
        )

        self._spectrum_axes.clear()
        self._style_signal_axes(self._spectrum_axes)
        peak_labels = []
        for values, label, color in (
                (self._data_a[:preview_length], "通道 A", "#2563eb"),
                (self._data_b[:preview_length], "通道 B", "#f97316"),
        ):
            frequencies, amplitudes = spectrum(values, sample_rate)
            if not frequencies.size:
                continue
            peak_index = int(amplitudes.argmax())
            peak_frequency = float(frequencies[peak_index])
            self._spectrum_axes.plot(
                frequencies, amplitudes, color=color, linewidth=1.1, label=label
            )
            self._spectrum_axes.scatter(
                [peak_frequency], [amplitudes[peak_index]],
                color=color, s=22, zorder=3,
            )
            peak_labels.append(f"{label} {peak_frequency:.1f} Hz")

        font_properties = self._plot_font_properties()
        foreground = self.palette().windowText().color().name()
        self._spectrum_axes.set_xlabel(
            "频率 (Hz)", color=foreground, fontproperties=font_properties
        )
        self._spectrum_axes.set_ylabel(
            "幅值", color=foreground, fontproperties=font_properties
        )
        self._spectrum_axes.set_xlim(0, 3000)
        if self._spectrum_axes.lines:
            legend = self._spectrum_axes.legend(
                loc="upper right", fontsize=8, prop=font_properties
            )
            for label in legend.get_texts():
                label.set_color(self.palette().windowText().color().name())
        self._spectrum_figure.tight_layout(pad=0.35)
        self._spectrum_canvas.draw_idle()
        self.ui.signalLegendRange.setText(
            "频谱峰值：" + " · ".join(peak_labels) if peak_labels else "频谱暂无有效数据"
        )

    def _draw_signal_axis(self, figure, canvas, axes, x_values, y_values,
                          x_label, y_label, color):
        axes.clear()
        self._style_signal_axes(axes)
        axes.plot(x_values, y_values, color=color, linewidth=0.75)
        font_properties = self._plot_font_properties()
        foreground = self.palette().windowText().color().name()
        axes.set_xlabel(x_label, color=foreground, fontproperties=font_properties)
        axes.set_ylabel(y_label, color=foreground, fontproperties=font_properties)
        figure.tight_layout(pad=0.25)
        canvas.draw_idle()

    def _style_signal_axes(self, axes):
        background = self.palette().window().color().name()
        foreground = self.palette().windowText().color().name()
        axes.set_facecolor(background)
        axes.figure.patch.set_facecolor(background)
        axes.tick_params(colors=foreground, labelsize=8)
        axes.grid(True, color="#94a3b8", alpha=0.22, linewidth=0.7)
        for spine in axes.spines.values():
            spine.set_color("#94a3b8")
            spine.set_alpha(0.45)

    @staticmethod
    def _plot_font_properties():
        font_path = next((path for path in (
            Path(r"C:\Windows\Fonts\msyh.ttc"),
            Path(r"C:\Windows\Fonts\simhei.ttf"),
        ) if path.exists()), None)
        return FontProperties(fname=str(font_path)) if font_path else None

    def _draw_localization_result(self, result, distance):
        self._correlation_figure.clear()
        axes = self._correlation_figure.subplots()

        background = self.palette().window().color().name()
        foreground = self.palette().windowText().color().name()
        font_properties = self._plot_font_properties()
        axes.set_facecolor(background)
        self._correlation_figure.patch.set_facecolor(background)

        best_trace = None
        for low, high, distance_axis, coefficients in result.traces or []:
            is_best = (low, high) == (result.best_low, result.best_high)
            line, = axes.plot(
                distance_axis,
                coefficients,
                color="#2563eb" if is_best else "#94a3b8",
                linewidth=2.2 if is_best else 1.0,
                alpha=1.0 if is_best else 0.48,
                label=f"最优频段 {low}-{high} Hz" if is_best else None,
                zorder=3 if is_best else 1,
            )
            if is_best:
                best_trace = (distance_axis, coefficients, line.get_color())

        if best_trace is not None:
            distance_axis, coefficients, color = best_trace
            peak_index = int(abs(distance_axis - result.dis_a).argmin())
            axes.axvline(result.dis_a, color="#f97316", linestyle="--",
                         linewidth=1.4, alpha=0.9, zorder=4)
            axes.scatter(
                [distance_axis[peak_index]], [coefficients[peak_index]],
                color="#f97316", edgecolors="white", linewidths=0.8,
                s=42, zorder=5, label=f"定位点 {result.dis_a:.2f} m",
            )

        axes.set_xlim(0, distance)
        axes.set_ylim(0, 1.05)
        axes.set_xlabel("距传感器 A 的距离 (m)", color=foreground,
                        fontproperties=font_properties)
        axes.set_ylabel("|相关系数|", color=foreground,
                        fontproperties=font_properties)
        axes.tick_params(colors=foreground, labelsize=8)
        axes.grid(True, color="#94a3b8", alpha=0.22, linewidth=0.7)
        for spine in axes.spines.values():
            spine.set_color("#94a3b8")
            spine.set_alpha(0.45)
        legend = axes.legend(loc="upper right", fontsize=8, framealpha=0.75,
                             prop=font_properties)
        if legend:
            legend.get_frame().set_facecolor(background)
            legend.get_frame().set_edgecolor("#94a3b8")
            for label in legend.get_texts():
                label.set_color(foreground)

        self._correlation_figure.tight_layout(pad=0.35)
        self._correlation_canvas.draw_idle()
        self._correlation_canvas.show()

    @staticmethod
    def _amplitude_range(values):
        if not values:
            return "-"
        return f"{min(values):.4f} ~ {max(values):.4f}"

    @staticmethod
    def _parse_data_file(file_path):
        with open(file_path, "r", encoding="utf-8-sig") as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            raise ValueError("数据文件为空")

        separator = next(
            (index for index, line in enumerate(lines)
             if line.startswith("=") or line in ("-", "---")),
            None,
        )

        numeric_lines = []
        if separator is not None:
            first = lines[0]
            try:
                float(first)
                data_start = 0
            except ValueError:
                data_start = 1

            separator_text = lines[separator]
            a_lines = lines[data_start:separator]
            b_lines = lines[separator + 1:]
        else:
            # 支持：首行为时间记录的格式，以及纯数值前后平分的格式
            try:
                float(lines[0])
                a_lines = []
                b_lines = []
                numeric_lines = lines
            except ValueError:
                numeric_lines = lines[1:] if len(lines) > 1 else []

            if not numeric_lines:
                raise ValueError("未找到有效数值数据")

            middle = len(numeric_lines) // 2
            if len(numeric_lines) % 2:
                raise ValueError("纯数值数据应能平均分成 A、B 两个通道")
            a_lines = numeric_lines[:middle]
            b_lines = numeric_lines[middle:]

        try:
            data_a = [float(line.replace(",", "")) for line in a_lines]
            data_b = [float(line.replace(",", "")) for line in b_lines]
        except ValueError as exc:
            raise ValueError(f"数据文件包含非数值内容：{exc}") from exc

        if not data_a or not data_b:
            raise ValueError("缺少 A/B 通道数据，请检查分隔行或数据格式")
        if len(data_a) != len(data_b):
            raise ValueError(
                f"A/B 通道数据长度不一致（A: {len(data_a)}，B: {len(data_b)}）"
            )

        return data_a, data_b

    def _apply_config(self, config):
        applied = 0

        material = config.get("PipeMaterial", config.get("material"))
        if isinstance(material, str) and material.strip():
            index = self.ui.cfgMaterial.findText(material)
            if index < 0:
                self.ui.cfgMaterial.addItem(material)
                index = self.ui.cfgMaterial.findText(material)
            self.ui.cfgMaterial.setCurrentIndex(index)
            applied += 1

        for keys, widget, cast in (
                (("PipeLength", "distance"), self.ui.cfgDis, float),
                (("PipeDiameter", "diameter"), self.ui.cfgDiam, int),
                (("MaxFrequency", "maxFrequency", "freqMax"), self.ui.cfgFreqMax, float),
                (("MinFrequency", "minFrequency", "freqMin"), self.ui.cfgFreqMin, float),
                (("Velocity", "velocity"), self.ui.cfgVelo, float),
        ):
            value = next((config[key] for key in keys if key in config), None)
            if value is None:
                continue
            try:
                converted = cast(value)
            except (TypeError, ValueError):
                continue
            widget.setValue(converted)
            applied += 1

        return applied

    def _default_velocity_entries(self):
        return [
            ("铸铁", 0, 99, 1320), ("铸铁", 100, 199, 1250),
            ("铸铁", 200, 299, 1190), ("铸铁", 300, 399, 1160),
            ("铸铁", 400, 599, 1130), ("铸铁", 600, 799, 1080),
            ("铸铁", 800, 899, 1060), ("铸铁", 1000, -1, 1030),
            ("钢", 0, 99, 1280), ("钢", 100, 199, 1220),
            ("钢", 200, 299, 1160), ("钢", 300, 399, 1130),
            ("钢", 400, 499, 1100), ("钢", 500, 699, 1080),
            ("钢", 700, -1, 1030),
            ("球墨铸铁", 0, 49, 1300), ("球墨铸铁", 50, 99, 1280),
            ("球墨铸铁", 100, 199, 1210), ("球墨铸铁", 200, 399, 1180),
            ("球墨铸铁", 400, 799, 1160), ("球墨铸铁", 800, 1199, 1150),
            ("球墨铸铁", 1200, 1999, 1150), ("球墨铸铁", 2000, -1, 1140),
            ("PVC", 0, 17, 650), ("PVC", 18, 22, 630),
            ("PVC", 23, 27, 600), ("PVC", 28, 49, 540),
            ("PVC", 50, 74, 520), ("PVC", 75, 99, 480),
            ("PVC", 100, 199, 460), ("PVC", 200, -1, 440),
            ("HDPE", 0, 17, 360), ("HDPE", 18, 22, 330),
            ("HDPE", 23, 74, 300), ("HDPE", 75, 199, 300),
            ("HDPE", 200, -1, 300),
        ]

    def _refresh_materials(self):
        materials = []
        for material, _, _, _ in self._velocity_entries:
            if material not in materials:
                materials.append(material)

        current = self.ui.cfgMaterial.currentText()
        self.ui.cfgMaterial.blockSignals(True)
        self.ui.cfgMaterial.clear()
        self.ui.cfgMaterial.addItems(materials)
        index = self.ui.cfgMaterial.findText(current)
        self.ui.cfgMaterial.setCurrentIndex(index if index >= 0 else 0)
        self.ui.cfgMaterial.blockSignals(False)

    def match_velocity(self):
        material = self.ui.cfgMaterial.currentText()
        diameter = int(self.ui.cfgDiam.value())
        best_match = None

        for entry_material, low, high, velocity in self._velocity_entries:
            if entry_material != material:
                continue
            if diameter >= low and (high < 0 or diameter <= high):
                best_match = velocity
                break

        if best_match is not None:
            self.ui.cfgVelo.setValue(best_match)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
