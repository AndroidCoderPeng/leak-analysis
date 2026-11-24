"""漏水信号分析与相关定位核心算法。

由原 data_analysis.py 迁移而来，纯 numpy/scipy 实现，与任何界面框架无关。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy import signal

SAMPLE_RATE = 7500.0
CUT_LOW = 0.8
CUT_HIGH = 1.2

#: 默认扫描频段（Hz）
DEFAULT_BANDS = [
    (100, 300), (200, 500), (400, 800), (600, 1200),
    (800, 1600), (1000, 2000), (1200, 3000),
]

@dataclass
class LocateResult:
    ok: bool = False
    dis_a: float = -1.0
    dis_b: float = -1.0
    snr: float = 0.0
    coefficient: float = 0.0
    time_diff: float = 0.0
    best_low: int = 0
    best_high: int = 0
    bands_used: int = 0
    traces: list[tuple[int, int, np.ndarray, np.ndarray]] | None = None


def de_mean(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size:
        arr = np.nan_to_num(arr, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
    return arr - np.mean(arr) if arr.size else arr


def chebyshev2_bandpass(values: Iterable[float], low: float, high: float,
                        fs: float = SAMPLE_RATE) -> np.ndarray:
    x = np.asarray(values, dtype=np.float64)
    x = np.nan_to_num(x, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
    if x.size == 0:
        return x

    cut_low = low * CUT_LOW
    cut_high = high * CUT_HIGH
    if cut_low <= 0 or cut_high >= fs / 2 or cut_low >= cut_high:
        return x.copy()

    wp = [cut_low / (fs / 2), cut_high / (fs / 2)]
    ws = [max(0.001, cut_low * 0.9 / (fs / 2)),
          min(0.999, cut_high * 1.1 / (fs / 2))]

    try:
        order, wn = signal.cheb2ord(wp, ws, 0.5, 40.0)
        b, a = signal.cheby2(order, 40.0, wn, btype="bandpass")
        if len(b) > len(x):
            return x.copy()
        return signal.filtfilt(b, a, x)
    except (ValueError, RuntimeError):
        return x.copy()


def pearson_overlap(a: np.ndarray, b: np.ndarray, offset: int) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0

    a_start = max(0, offset)
    a_end = min(a.size, offset + b.size)
    length = a_end - a_start
    if length < 2:
        return 0.0

    segment_a = np.asarray(a[a_start:a_end], dtype=np.float64)
    segment_b = np.asarray(b[0:length], dtype=np.float64)
    if not np.all(np.isfinite(segment_a)) or not np.all(np.isfinite(segment_b)):
        return 0.0

    scale_a = float(np.max(np.abs(segment_a)))
    scale_b = float(np.max(np.abs(segment_b)))
    if scale_a <= 1e-15 or scale_b <= 1e-15:
        return 0.0

    segment_a = segment_a / scale_a
    segment_b = segment_b / scale_b
    da = segment_a - np.mean(segment_a)
    db = segment_b - np.mean(segment_b)

    var_a = float(np.dot(da, da))
    var_b = float(np.dot(db, db))
    if not np.isfinite(var_a) or not np.isfinite(var_b):
        return 0.0
    if var_a <= 1e-15 or var_b <= 1e-15:
        return 0.0

    covariance = float(np.dot(da, db))
    denominator = np.sqrt(var_a * var_b)
    if not np.isfinite(covariance) or not np.isfinite(denominator) or denominator <= 1e-15:
        return 0.0

    coefficient = covariance / denominator
    if not np.isfinite(coefficient):
        return 0.0
    return float(np.clip(coefficient, -1.0, 1.0))


def correlation_vector(a: np.ndarray, b: np.ndarray, distance: float,
                       velocity: float, fs: float = SAMPLE_RATE):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.size == 0 or a.size != b.size or distance <= 0 or velocity <= 0 or fs <= 0:
        return np.array([]), np.array([])

    sampling_interval_us = 1e6 / fs
    max_time_diff_us = distance / velocity * 1e6
    max_lag = int(np.floor(max_time_diff_us / sampling_interval_us))
    point_num = 1 + 2 * max_lag
    center = max_lag

    corr = np.zeros(point_num, dtype=np.float64)
    dis_axis = np.zeros(point_num, dtype=np.float64)

    for i in range(max_lag + 1):
        corr[center - i] = pearson_overlap(a, b, i)
        corr[center + i] = pearson_overlap(b, a, i)
        half = velocity * sampling_interval_us / 2.0 * i * 1e-6
        dis_axis[center - i] = distance / 2.0 - half
        dis_axis[center + i] = distance / 2.0 + half

    return corr, dis_axis


def evaluate_band(a: Iterable[float], b: Iterable[float], distance: float,
                  velocity: float, low: int, high: int, fs: float = SAMPLE_RATE):
    vec_a = chebyshev2_bandpass(de_mean(a), low, high, fs)
    vec_b = chebyshev2_bandpass(de_mean(b), low, high, fs)
    corr, dis_axis = correlation_vector(vec_a, vec_b, distance, velocity, fs)

    result = LocateResult(best_low=low, best_high=high)
    if corr.size == 0:
        return result, corr, dis_axis

    abs_corr = np.abs(corr)
    mean_corr = float(np.mean(abs_corr))
    if mean_corr <= 1e-12:
        return result, corr, dis_axis

    max_index = int(np.argmax(abs_corr))
    coefficient = float(abs_corr[max_index])
    dis_a = round(float(dis_axis[max_index]) * 100.0) / 100.0
    dis_b = distance - dis_a

    result.ok = True
    result.coefficient = coefficient
    result.snr = coefficient / mean_corr
    result.dis_a = dis_a
    result.dis_b = dis_b
    result.time_diff = (dis_a - dis_b) / velocity
    return result, corr, dis_axis


def locate(a: Iterable[float], b: Iterable[float], distance: float,
           velocity: float, bands: Iterable[tuple[float, float]],
           fs: float = SAMPLE_RATE) -> LocateResult:
    vec_a = np.asarray(a, dtype=np.float64)
    vec_b = np.asarray(b, dtype=np.float64)
    if vec_a.size == 0 or vec_a.size != vec_b.size or distance <= 0 or velocity <= 0:
        return LocateResult()

    bands = [(int(low), int(high)) for low, high in bands
             if 0 < float(low) < float(high) and float(high) < fs / 2]
    if not bands:
        return LocateResult()

    traces = []
    best = LocateResult()
    snr_max = -1.0

    for low, high in bands:
        result, corr, dis_axis = evaluate_band(vec_a, vec_b, distance, velocity, low, high, fs)
        if corr.size:
            traces.append((low, high, dis_axis, np.abs(corr)))
        if result.ok and result.snr > snr_max:
            snr_max = result.snr
            best = result

    if not best.ok:
        return LocateResult(bands_used=len(traces), traces=traces)

    final, _, _ = evaluate_band(vec_a, vec_b, distance, velocity,
                                best.best_low, best.best_high, fs)
    final.bands_used = len(traces)
    final.traces = traces
    return final


def spectrum(values: Iterable[float], fs: float = SAMPLE_RATE,
             max_frequency: float = 3000.0):
    x = np.asarray(values, dtype=np.float64)
    n = 1 << (x.size.bit_length() - 1)
    if n < 2:
        return np.array([]), np.array([])

    segment = x[:n] - np.mean(x[:n])
    spectrum_values = np.fft.rfft(segment)
    frequencies = np.fft.rfftfreq(n, d=1.0 / fs)
    amplitudes = np.abs(spectrum_values) * 2.0 / n
    mask = frequencies <= max_frequency
    return frequencies[mask], amplitudes[mask]


def filter_bands(bands, freq_min: float = 0.0, freq_max: float = 0.0):
    """按用户指定的频率范围筛选扫描频段，逻辑与原界面版一致。"""
    if freq_min > 0 or freq_max > 0:
        bands = [band for band in bands
                 if band[0] >= freq_min and band[1] <= freq_max]
    if not bands:
        bands = [(freq_min, freq_max)]
    return bands
