"""LeakAnalysis 命令行入口。

用法示例：

    python cli.py data/测试数据.txt
    python cli.py data/测试数据.txt --config data/参数配置.json --output report
    python cli.py data.txt -d 209 -v 1130 --freq-min 100 --freq-max 3000
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.analysis import DEFAULT_BANDS, SAMPLE_RATE, filter_bands, locate
from core.io import (
    AnalysisParams,
    apply_config,
    load_config,
    parse_data_file,
    validate_params,
)
from core.materials import load_velocity_table, match_velocity
from report import plot_correlation, plot_spectrum, plot_waveforms, write_result_json

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_VELOCITY_TABLE = PROJECT_ROOT / "config" / "velocity_table.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="leak-analysis",
        description="漏水信号分析与相关定位（命令行版）",
    )
    parser.add_argument("data_file", help="A/B 双通道数据文件（.txt / .dat）")
    parser.add_argument("-c", "--config", help="JSON 参数配置文件")
    parser.add_argument("-o", "--output", default="report",
                        help="报告输出目录（默认 report）")
    parser.add_argument("-d", "--distance", type=float, help="传感器间距 (m)")
    parser.add_argument("-v", "--velocity", type=float, help="声速 (m/s)")
    parser.add_argument("--material", help="管材名称（用于自动匹配声速）")
    parser.add_argument("--diameter", type=int, help="管径 (mm)（用于自动匹配声速）")
    parser.add_argument("--freq-min", type=float, help="最小频率 (Hz)")
    parser.add_argument("--freq-max", type=float, help="最大频率 (Hz)")
    parser.add_argument("--sample-rate", type=float, default=SAMPLE_RATE,
                        help=f"采样率 (Hz，默认 {SAMPLE_RATE:g})")
    parser.add_argument("--duration", type=float, default=10.0,
                        help="参与计算的信号时长 (s，默认 10)")
    parser.add_argument("--velocity-table",
                        default=str(DEFAULT_VELOCITY_TABLE) if DEFAULT_VELOCITY_TABLE.exists() else "",
                        help="管材声速表 JSON（默认 config/velocity_table.json）")
    parser.add_argument("--no-plots", action="store_true",
                        help="只输出结果，不生成图片")
    return parser


def resolve_params(args) -> AnalysisParams:
    """合成参数：命令行 > 配置文件 > 默认值；再尝试材料+管径匹配声速。"""
    params = AnalysisParams(sample_rate=args.sample_rate, duration=args.duration)

    if args.config:
        applied = apply_config(params, load_config(args.config))
        print(f"已加载配置：{args.config}（应用 {applied} 项）")

    if args.distance is not None:
        params.distance = args.distance
    if args.velocity is not None:
        params.velocity = args.velocity
    if args.material:
        params.material = args.material
    if args.diameter is not None:
        params.diameter = args.diameter
    if args.freq_min is not None:
        params.freq_min = args.freq_min
    if args.freq_max is not None:
        params.freq_max = args.freq_max

    # 声速未明确指定时，尝试按材料 + 管径从声速表匹配
    if not params.velocity_known() and params.material and params.diameter > 0:
        velocity = _match_velocity_from_table(args.velocity_table,
                                              params.material, params.diameter)
        if velocity is not None:
            params.velocity = velocity
            print(f"已按声速表匹配声速：{params.material} DN{params.diameter} "
                  f"→ {velocity:g} m/s")
    return params


def _match_velocity_from_table(table_path: str, material: str,
                               diameter: int) -> float | None:
    if not table_path:
        return None
    try:
        entries = load_velocity_table(table_path)
    except (OSError, ValueError):
        return None
    return match_velocity(entries, material, diameter)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    data_path = Path(args.data_file)
    if not data_path.exists():
        print(f"错误：数据文件不存在：{data_path}", file=sys.stderr)
        return 2

    try:
        data_a, data_b = parse_data_file(data_path)
    except (OSError, ValueError) as exc:
        print(f"错误：数据导入失败：{exc}", file=sys.stderr)
        return 2

    params = resolve_params(args)

    problems = validate_params(params)
    if len(data_a) != len(data_b):
        problems.append(f"A/B 通道数据长度不一致（A: {len(data_a)}，B: {len(data_b)}）")
    if problems:
        print("错误：参数校验未通过：", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 2

    length = min(len(data_a), len(data_b))
    use_length = min(int(params.duration * params.sample_rate), length)
    duration_actual = use_length / params.sample_rate
    print(f"数据：{data_path.name}（A/B 各 {len(data_a)} 点，"
          f"计算前 {duration_actual:.1f} s @ {params.sample_rate:g} Hz）")

    bands = filter_bands(DEFAULT_BANDS, params.freq_min, params.freq_max)
    print(f"参数：距离 {params.distance:g} m，声速 {params.velocity:g} m/s，"
          f"扫描频段 {bands[0][0]}-{bands[-1][1]} Hz 共 {len(bands)} 档")

    result = locate(data_a[:use_length], data_b[:use_length],
                    params.distance, params.velocity, bands, params.sample_rate)

    if not result.ok:
        print("定位失败：没有有效频段参与计算，请检查参数和频段范围", file=sys.stderr)
        return 1

    print("定位成功：")
    print(f"  距传感器 A：{result.dis_a:.2f} m")
    print(f"  距传感器 B：{result.dis_b:.2f} m")
    print(f"  时差：{result.time_diff * 1000:.2f} ms")
    print(f"  最优频段：{result.best_low}-{result.best_high} Hz"
          f"（扫描 {result.bands_used} 档）")
    print(f"  峰值相关系数：{result.coefficient:.4f}，SNR：{result.snr:.2f}")
    print(f"  定位可信度：{'可信（SNR ≥ 6）' if result.flag else '不可信（SNR < 6）'}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = write_result_json(out_dir, result, params, str(data_path))
    print(f"结果已写入：{json_path}")

    if not args.no_plots:
        try:
            paths = [
                plot_waveforms(out_dir, data_a, data_b,
                               params.sample_rate, params.duration),
                plot_spectrum(out_dir, data_a, data_b, params.sample_rate,
                              params.duration),
                plot_correlation(out_dir, result, params.distance),
            ]
        except Exception as exc:  # 图片生成失败不影响结果输出
            print(f"警告：图片生成失败：{exc}", file=sys.stderr)
        else:
            for path in paths:
                print(f"图片已生成：{path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
