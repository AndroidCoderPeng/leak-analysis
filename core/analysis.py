"""漏水信号分析与相关定位核心算法。

由原 data_analysis.py 迁移而来，纯 numpy/scipy 实现，与任何界面框架无关。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy import signal

SAMPLE_RATE = 7500.0
#: 阻带边界系数：阻带 = [0.8*low, 1.2*high]（与 MATLAB bandp.m 一致）
CUT_LOW = 0.8
CUT_HIGH = 1.2
#: 通带纹波 (dB) 与阻带衰减 (dB)（与 MATLAB bandp.m 内部固定值一致）
PASS_RIPPLE_DB = 1.0
STOP_ATTEN_DB = 40.0
#: 定位有效性阈值：SNR 低于该值视为不可信（与 MATLAB locating.m 的 flag 判据一致）
SNR_VALID_THRESHOLD = 6.0
#: 每个时延点参与相关计算的固定窗口，对应 7500 Hz 时的 5000 点。
CORRELATION_WINDOW_SECONDS = 5000.0 / SAMPLE_RATE

#: 与 algo-compare/freList_modified.xlsx Sheet2 一致的扫描频段。
DEFAULT_BANDS = [
    (100, 400), (100, 500), (100, 600), (100, 700), (100, 800),
    (100, 900), (100, 1000), (100, 1100), (100, 1200), (100, 1300),
    (100, 1400), (100, 1500), (100, 1600), (100, 1700), (100, 1800),
    (100, 1900), (100, 2000), (100, 2100), (100, 2200), (100, 2300),
    (100, 2400), (100, 2500), (55, 150), (70, 125), (60, 200),
    (75, 300), (80, 350), (60, 400), (110, 500),
]

@dataclass
class LocateResult:
    ok: bool = False
    flag: bool = False  # SNR >= SNR_VALID_THRESHOLD 时为 True（定位可信）
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

    wp = [low / (fs / 2), high / (fs / 2)]
    ws = [low * CUT_LOW / (fs / 2), high * CUT_HIGH / (fs / 2)]
    if min(wp) <= 0 or max(wp) >= 1 or min(wp) >= max(wp):
        return x.copy()

    try:
        order, wn = signal.cheb2ord(wp, ws, PASS_RIPPLE_DB, STOP_ATTEN_DB)
        sos = signal.cheby2(
            order, STOP_ATTEN_DB, wn, btype="bandpass", output="sos"
        )
        return signal.sosfiltfilt(sos, x)
    except (ValueError, RuntimeError):
        return x.copy()


def pearson_overlap(a: np.ndarray, b: np.ndarray, offset: int,
                    max_samples: int | None = None) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0

    a_start = max(0, offset)
    a_end = min(a.size, offset + b.size)
    length = a_end - a_start
    if max_samples is not None:
        length = min(length, max(0, max_samples))
    if length < 2:
        return 0.0

    segment_a = np.asarray(a[a_start:a_start + length], dtype=np.float64)
    segment_b = np.asarray(b[:length], dtype=np.float64)
    if not np.all(np.isfinite(segment_a)) or not np.all(np.isfinite(segment_b)):
        return 0.0

    scale_a = float(np.max(np.abs(segment_a)))
    scale_b = float(np.max(np.abs(segment_b)))
    if scale_a <= 1e-15 or scale_b <= 1e-15:
        return 0.0

    da = segment_a / scale_a
    db = segment_b / scale_b
    da = da - np.mean(da)
    db = db - np.mean(db)
    variance_a = float(np.dot(da, da))
    variance_b = float(np.dot(db, db))
    if variance_a <= 1e-15 or variance_b <= 1e-15:
        return 0.0

    coefficient = float(np.dot(da, db)) / np.sqrt(variance_a * variance_b)
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
    correlation_window_samples = max(
        2, int(round(CORRELATION_WINDOW_SECONDS * fs))
    )

    corr = np.zeros(point_num, dtype=np.float64)
    dis_axis = np.zeros(point_num, dtype=np.float64)

    for i in range(max_lag + 1):
        corr[center - i] = pearson_overlap(
            b, a, i, correlation_window_samples
        )
        corr[center + i] = pearson_overlap(
            a, b, i, correlation_window_samples
        )
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
    result.flag = result.snr >= SNR_VALID_THRESHOLD
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
             min_frequency: float = 20.0, max_frequency: float = 3000.0):
    """与 MATLAB getFreWave.m 一致：全长 FFT，返回 min~max 频率范围内的幅值。"""
    x = np.asarray(values, dtype=np.float64)
    n = x.size
    if n < 2:
        return np.array([]), np.array([])

    spectrum_values = np.fft.rfft(x)
    frequencies = np.fft.rfftfreq(n, d=1.0 / fs)
    amplitudes = np.abs(spectrum_values) * 2.0 / n
    mask = (frequencies >= min_frequency) & (frequencies <= max_frequency)
    return frequencies[mask], amplitudes[mask]


def filter_bands(bands, freq_min: float = 0.0, freq_max: float = 0.0):
    """按用户指定的频率范围筛选扫描频段，逻辑与原界面版一致。"""
    if freq_min > 0 or freq_max > 0:
        bands = [band for band in bands
                 if band[0] >= freq_min and band[1] <= freq_max]
    if not bands:
        bands = [(freq_min, freq_max)]
    return bands
