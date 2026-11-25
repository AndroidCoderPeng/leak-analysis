"""数据文件解析与参数配置加载。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class AnalysisParams:
    """一次定位计算所需的全部参数。"""
    distance: float = 0.0  # 传感器间距 (m)
    velocity: float = 0.0  # 声速 (m/s)
    diameter: int = 0  # 管径 (mm)
    material: str = ""  # 管材
    freq_min: float = 0.0  # 最小频率 (Hz)，0 表示不限
    freq_max: float = 0.0  # 最大频率 (Hz)，0 表示不限
    sample_rate: float = 7500.0  # 采样率 (Hz)
    duration: float = 10.0  # 参与计算的信号时长 (s)
    band_mode: str = "regular"  # regular: Sheet2；high: Sheet1

    def velocity_known(self) -> bool:
        return self.velocity > 0


def parse_data_file(file_path: str | Path) -> tuple[list[float], list[float]]:
    """解析 A/B 双通道文本数据文件。

    支持的格式（与原界面版一致）：
    - 时间戳行 / 表头行 + 数值数据，可选 `=` 或 `-` 分隔行区分 A、B 通道；
    - 无分隔行时，纯数值前后对半分为 A、B 两个通道。
    """
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


def load_config(file_path: str | Path) -> dict[str, Any]:
    """读取 JSON 参数配置文件，返回字典。"""
    with open(file_path, "r", encoding="utf-8-sig") as file:
        config = json.load(file)
    if not isinstance(config, dict):
        raise ValueError("配置文件根节点必须为 JSON 对象")
    return config


def apply_config(params: AnalysisParams, config: dict[str, Any]) -> int:
    """把配置文件中的字段应用到参数对象，返回成功应用的字段数。

    兼容原界面版识别的全部键名，数值字段允许字符串形式。
    """
    applied = 0
    if any(key in config for key in (
            "LowFrequency", "lowFrequency", "HighFrequency", "highFrequency")):
        params.band_mode = "high"

    def take_int(value) -> int:
        return int(float(value))

    material = config.get("PipeMaterial", config.get("material"))
    if isinstance(material, str) and material.strip():
        params.material = material.strip()
        applied += 1

    for keys, field_name, cast in (
            (("PipeLength", "distance"), "distance", float),
            (("PipeDiameter", "diameter"), "diameter", take_int),
            (("MaxFrequency", "maxFrequency", "freqMax",
              "HighFrequency", "highFrequency"), "freq_max", float),
            (("MinFrequency", "minFrequency", "freqMin",
              "LowFrequency", "lowFrequency"), "freq_min", float),
            (("Velocity", "velocity"), "velocity", float),
    ):
        value = next((config[key] for key in keys if key in config), None)
        if value is None:
            continue
        try:
            converted = cast(value)
        except (TypeError, ValueError):
            continue
        setattr(params, field_name, converted)
        applied += 1

    return applied


def validate_params(params: AnalysisParams) -> list[str]:
    """校验参数，返回问题列表（为空表示通过）。"""
    problems = []
    if params.distance <= 0:
        problems.append("传感器距离必须大于 0")
    if params.freq_min > params.freq_max:
        problems.append("最小频率不能大于最大频率")
    if params.velocity <= 0:
        problems.append("声速必须大于 0（可通过材料+管径自动匹配，或命令行指定）")
    elif params.velocity < 100 or params.velocity > 6000:
        problems.append("声速超出合理范围（100 ~ 6000 m/s）")
    return problems
