import unittest
from pathlib import Path

import numpy as np

from core.analysis import chebyshev2_bandpass, correlation_vector, evaluate_band
from core.io import AnalysisParams, apply_config, parse_data_file


class CorrelationVectorTests(unittest.TestCase):
    def test_delayed_a_maps_to_greater_distance_from_sensor_a(self):
        base = np.random.default_rng(7).normal(size=2000)
        lag = 20
        a = np.concatenate((np.zeros(lag), base[:-lag]))
        b = base.copy()

        correlation, distance = correlation_vector(
            a, b, distance=200.0, velocity=1000.0, fs=10000.0
        )

        self.assertGreater(distance[np.argmax(correlation)], 100.0)


class BandpassTests(unittest.TestCase):
    def test_narrow_low_frequency_filter_remains_finite(self):
        values = np.random.default_rng(7).normal(size=7500)

        filtered = chebyshev2_bandpass(values, 60.0, 200.0, fs=7500.0)

        self.assertTrue(np.isfinite(filtered).all())
        self.assertLess(np.max(np.abs(filtered)), 100.0)


class ReportSampleTests(unittest.TestCase):
    def test_report_distances_stay_close_to_verified_results(self):
        root = Path(__file__).resolve().parents[1]
        cases = [
            ("测试报告20260319.57", "测试数据.57.160526.txt", (60, 200), 110.61),
            ("测试报告20260319.60", "测试数据.60.160725.txt", (110, 500), 97.54),
            ("测试报告20260319.61", "测试数据.61.160815.txt", (60, 200), 105.04),
            ("测试报告20260319.62", "测试数据.62.160852.txt", (60, 200), 111.46),
            ("测试报告20260319.65", "测试数据.65.161243.txt", (100, 400), 112.08),
            ("测试报告20261124.8", "测试数据.8.132407.txt", (1000, 1500), 99.16),
        ]

        for folder, filename, band, expected in cases:
            with self.subTest(folder=folder, band=band):
                data_a, data_b = parse_data_file(root / "data" / folder / filename)
                result, _, _ = evaluate_band(
                    data_a[:75000], data_b[:75000], 209.0, 1160.0, *band
                )
                self.assertTrue(result.ok)
                self.assertLessEqual(abs(result.dis_a - expected), 2.1)


class ApplyConfigTests(unittest.TestCase):
    def test_accepts_legacy_low_high_frequency_fields(self):
        params = AnalysisParams()

        applied = apply_config(
            params, {"LowFrequency": "100", "HighFrequency": "3000"}
        )

        self.assertEqual(applied, 2)
        self.assertEqual(params.freq_min, 100.0)
        self.assertEqual(params.freq_max, 3000.0)

    def test_primary_frequency_fields_take_precedence(self):
        params = AnalysisParams()

        apply_config(
            params,
            {
                "MinFrequency": "200",
                "LowFrequency": "100",
                "MaxFrequency": "2500",
                "HighFrequency": "3000",
            },
        )

        self.assertEqual(params.freq_min, 200.0)
        self.assertEqual(params.freq_max, 2500.0)


if __name__ == "__main__":
    unittest.main()
