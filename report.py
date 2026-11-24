"""结果报告生成：matplotlib Agg 后端输出 PNG 图片与 JSON 结果文件。"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 无窗口渲染，不依赖任何界面框架

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402

from core.analysis import LocateResult, spectrum  # noqa: E402

COLOR_A = "#2563eb"
COLOR_B = "#f97316"
COLOR_BEST = "#2563eb"
COLOR_OTHER = "#94a3b8"
COLOR_MARKER = "#f97316"

FOREGROUND = "#1e293b"
GRID_COLOR = "#94a3b8"


def _font_properties() -> FontProperties | None:
    for path in (Path(r"C:\Windows\Fonts\msyh.ttc"),
                 Path(r"C:\Windows\Fonts\simhei.ttf")):
        if path.exists():
            return FontProperties(fname=str(path))
    return None


def _style_axes(axes):
    axes.tick_params(colors=FOREGROUND, labelsize=8)
    axes.grid(True, color=GRID_COLOR, alpha=0.22, linewidth=0.7)
    for spine in axes.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_alpha(0.45)
    font = _font_properties()
    if font:
        for label in (*axes.get_xticklabels(), *axes.get_yticklabels()):
            label.set_fontproperties(font)


def plot_waveforms(out_dir: Path, data_a, data_b, fs: float, duration: float) -> Path:
    """A/B 通道波形预览图。"""
    preview_length = min(int(duration * fs), len(data_a), len(data_b))
    time_axis = [index / fs for index in range(preview_length)]

    figure, axes = plt.subplots(figsize=(7, 2.6), tight_layout=True)
    axes.plot(time_axis, data_a[:preview_length], color=COLOR_A, linewidth=0.75,
              label="通道 A")
    axes.plot(time_axis, data_b[:preview_length], color=COLOR_B, linewidth=0.75,
              label="通道 B")
    axes.set_xlabel("时间 (s)", fontproperties=_font_properties(), color=FOREGROUND)
    axes.set_ylabel("幅值", fontproperties=_font_properties(), color=FOREGROUND)
    _style_axes(axes)
    legend = axes.legend(loc="upper right", fontsize=8, prop=_font_properties())
    if legend:
        for label in legend.get_texts():
            label.set_color(FOREGROUND)

    path = out_dir / "waveforms.png"
    figure.savefig(path, dpi=140)
    plt.close(figure)
    return path


def plot_spectrum(out_dir: Path, data_a, data_b, fs: float,
                  duration: float, max_frequency: float = 3000.0) -> Path:
    """A/B 通道频谱图，标注峰值频率。"""
    preview_length = min(int(duration * fs), len(data_a), len(data_b))
    peak_labels = []

    figure, axes = plt.subplots(figsize=(7, 2.6), tight_layout=True)
    for values, label, color in (
            (data_a[:preview_length], "通道 A", COLOR_A),
            (data_b[:preview_length], "通道 B", COLOR_B),
    ):
        frequencies, amplitudes = spectrum(values, fs,
                                           max_frequency=max_frequency)
        if not frequencies.size:
            continue
        peak_index = int(amplitudes.argmax())
        peak_frequency = float(frequencies[peak_index])
        axes.plot(frequencies, amplitudes, color=color, linewidth=1.1, label=label)
        axes.scatter([peak_frequency], [amplitudes[peak_index]],
                     color=color, s=22, zorder=3)
        peak_labels.append(f"{label} {peak_frequency:.1f} Hz")

    axes.set_xlabel("频率 (Hz)", fontproperties=_font_properties(), color=FOREGROUND)
    axes.set_ylabel("幅值", fontproperties=_font_properties(), color=FOREGROUND)
    axes.set_xlim(0, max_frequency)
    _style_axes(axes)
    if axes.lines:
        legend = axes.legend(loc="upper right", fontsize=8, prop=_font_properties())
        if legend:
            for label in legend.get_texts():
                label.set_color(FOREGROUND)

    path = out_dir / "spectrum.png"
    figure.savefig(path, dpi=140)
    plt.close(figure)
    return path


def plot_correlation(out_dir: Path, result: LocateResult, distance: float) -> Path:
    """各频段相关系数-距离曲线，高亮最优频段与定位点。"""
    figure, axes = plt.subplots(figsize=(7, 3.2), tight_layout=True)

    best_trace = None
    for low, high, distance_axis, coefficients in result.traces or []:
        is_best = (low, high) == (result.best_low, result.best_high)
        line, = axes.plot(
            distance_axis,
            coefficients,
            color=COLOR_BEST if is_best else COLOR_OTHER,
            linewidth=2.2 if is_best else 1.0,
            alpha=1.0 if is_best else 0.48,
            label=f"最优频段 {low}-{high} Hz" if is_best else None,
            zorder=3 if is_best else 1,
        )
        if is_best:
            best_trace = (distance_axis, coefficients)

    if best_trace is not None:
        distance_axis, coefficients = best_trace
        peak_index = int(abs(distance_axis - result.dis_a).argmin())
        axes.axvline(result.dis_a, color=COLOR_MARKER, linestyle="--",
                     linewidth=1.4, alpha=0.9, zorder=4)
        axes.scatter(
            [distance_axis[peak_index]], [coefficients[peak_index]],
            color=COLOR_MARKER, edgecolors="white", linewidths=0.8,
            s=42, zorder=5, label=f"定位点 {result.dis_a:.2f} m",
        )

    axes.set_xlim(0, distance)
    axes.set_ylim(0, 1.05)
    axes.set_xlabel("距传感器 A 的距离 (m)",
                    fontproperties=_font_properties(), color=FOREGROUND)
    axes.set_ylabel("|相关系数|",
                    fontproperties=_font_properties(), color=FOREGROUND)
    _style_axes(axes)
    legend = axes.legend(loc="upper right", fontsize=8, framealpha=0.75,
                         prop=_font_properties())
    if legend:
        for label in legend.get_texts():
            label.set_color(FOREGROUND)

    path = out_dir / "correlation.png"
    figure.savefig(path, dpi=140)
    plt.close(figure)
    return path


def write_result_json(out_dir: Path, result: LocateResult, params,
                      data_file: str) -> Path:
    """写出结果 JSON（traces 数组不序列化，只保留结论性数据）。"""
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "data_file": data_file,
        "params": {
            "distance": params.distance,
            "velocity": params.velocity,
            "material": params.material,
            "diameter": params.diameter,
            "freq_min": params.freq_min,
            "freq_max": params.freq_max,
            "sample_rate": params.sample_rate,
            "duration": params.duration,
        },
        "result": {
            "ok": result.ok,
            "flag": result.flag,
            "dis_a": result.dis_a,
            "dis_b": result.dis_b,
            "snr": result.snr,
            "coefficient": result.coefficient,
            "time_diff": result.time_diff,
            "best_band": [result.best_low, result.best_high],
            "bands_used": result.bands_used,
        },
    }
    path = out_dir / "result.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return path
