from __future__ import annotations

import unittest

from zpe_mocap.cmu_benchmark import (
    baseline_table_rows,
    benchmark_table_rows,
    list_cmu_bvh_paths,
    select_round_robin_subset,
    select_successful_rows,
    summarize_clip_rows,
)


class CmuBenchmarkHelperTests(unittest.TestCase):
    def test_list_cmu_bvh_paths_filters_and_sorts(self) -> None:
        payload = {
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": "data/002/02_02.bvh", "type": "blob"},
                {"path": "data/001/01_01.bvh", "type": "blob"},
                {"path": "data/001", "type": "tree"},
            ]
        }

        self.assertEqual(
            list_cmu_bvh_paths(payload),
            ["data/001/01_01.bvh", "data/002/02_02.bvh"],
        )

    def test_select_round_robin_subset_spreads_subjects(self) -> None:
        paths = [
            "data/001/01_01.bvh",
            "data/001/01_02.bvh",
            "data/002/02_01.bvh",
            "data/002/02_02.bvh",
            "data/003/03_01.bvh",
        ]

        self.assertEqual(
            select_round_robin_subset(paths, 5),
            [
                "data/001/01_01.bvh",
                "data/002/02_01.bvh",
                "data/003/03_01.bvh",
                "data/001/01_02.bvh",
                "data/002/02_02.bvh",
            ],
        )

    def test_select_successful_rows_preserves_declared_selection_order(self) -> None:
        selected_paths = [
            "data/001/01_01.bvh",
            "data/002/02_01.bvh",
            "data/003/03_01.bvh",
            "data/004/04_01.bvh",
        ]
        rows = [
            {"cmu_path": "data/004/04_01.bvh", "zpe_ratio": 4.0},
            {"cmu_path": "data/003/03_01.bvh", "zpe_ratio": 3.0},
            {"cmu_path": "data/001/01_01.bvh", "zpe_ratio": 1.0},
        ]

        self.assertEqual(
            select_successful_rows(rows, selected_paths=selected_paths, target_sequences=2),
            [
                {"cmu_path": "data/001/01_01.bvh", "zpe_ratio": 1.0},
                {"cmu_path": "data/003/03_01.bvh", "zpe_ratio": 3.0},
            ],
        )

    def test_summarize_clip_rows_aggregates_metrics(self) -> None:
        rows = [
            {
                "cmu_path": "data/001/01_01.bvh",
                "fps": 60,
                "frames": 600,
                "joints": 30,
                "zpe_ratio": 12.0,
                "gzip_ratio": 10.0,
                "joint_angle_rmse_deg": 4.0,
                "mpjpe_mm": 20.0,
                "encoded_size_bytes": 100,
                "raw_bvh_float32_bytes": 1200,
            },
            {
                "cmu_path": "data/002/02_01.bvh",
                "fps": 120,
                "frames": 1200,
                "joints": 32,
                "zpe_ratio": 18.0,
                "gzip_ratio": 12.0,
                "joint_angle_rmse_deg": 6.0,
                "mpjpe_mm": 30.0,
                "encoded_size_bytes": 200,
                "raw_bvh_float32_bytes": 2400,
            },
        ]

        summary = summarize_clip_rows(rows, target_sequences=2)

        self.assertEqual(summary["completed_sequences"], 2)
        self.assertEqual(summary["total_frames"], 1800)
        self.assertAlmostEqual(summary["total_duration_hours"], (10.0 + 10.0) / 3600.0)
        self.assertAlmostEqual(summary["joint_count_mean"], 31.0)
        self.assertAlmostEqual(summary["zpe_ratio_mean"], 15.0)
        self.assertAlmostEqual(summary["gzip_ratio_mean"], 11.0)
        self.assertAlmostEqual(summary["joint_angle_rmse_deg_mean"], 5.0)
        self.assertAlmostEqual(summary["mpjpe_mm_mean"], 25.0)
        self.assertAlmostEqual(summary["zpe_vs_gzip_mean_multiplier"], 15.0 / 11.0)
        self.assertEqual(summary["zpe_beats_gzip_sequences"], 2)

    def test_table_rows_render_summary(self) -> None:
        summary = {
            "completed_sequences": 120,
            "joint_count_mean": 31.25,
            "total_frames": 345678,
            "zpe_ratio_mean": 17.125,
            "joint_angle_rmse_deg_mean": 85.5,
            "mpjpe_mm_mean": 42.25,
            "gzip_ratio_mean": 13.5,
            "zpe_vs_gzip_mean_multiplier": 1.2685185185,
        }

        benchmark_rows = benchmark_table_rows(summary)
        baseline_rows = baseline_table_rows(summary)

        self.assertEqual(benchmark_rows[0]["dataset"], "CMU MoCap public subset (120 sequences)")
        self.assertEqual(benchmark_rows[0]["ratio"], "17.1250x")
        self.assertEqual(baseline_rows[0]["baseline"], "gzip -9 vs raw BVH float32")
        self.assertEqual(baseline_rows[0]["improvement"], "1.2685x")


if __name__ == "__main__":
    unittest.main()
