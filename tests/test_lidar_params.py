import unittest

from lidar_params import LidarParams


class LidarParamsTest(unittest.TestCase):
    def test_derived_values(self):
        params = LidarParams(angular_resolution_deg=0.5, rotation_speed_rpm=600)

        self.assertEqual(params.points_per_revolution, 720)
        self.assertEqual(params.scan_frequency_hz, 10.0)
        self.assertAlmostEqual(params.scan_period_s, 0.1)

    def test_cluster_points_recommendation(self):
        params = LidarParams(angular_resolution_deg=1.0, rotation_speed_rpm=300)

        self.assertEqual(params.recommend_min_cluster_points(0.2, 5.0), 2)
        self.assertEqual(params.recommend_min_cluster_points(0.05, 20.0), 1)

        coarse = LidarParams(angular_resolution_deg=10.0, rotation_speed_rpm=300)
        tan_20_deg = 0.36397
        self.assertEqual(coarse.recommend_min_cluster_points(tan_20_deg, 1.0), 2)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            LidarParams(angular_resolution_deg=0, rotation_speed_rpm=300)

        with self.assertRaises(ValueError):
            LidarParams(angular_resolution_deg=0.5, rotation_speed_rpm=0)

        params = LidarParams(angular_resolution_deg=0.5, rotation_speed_rpm=600)
        with self.assertRaises(ValueError):
            params.recommend_min_cluster_points(0, 5.0)
        with self.assertRaises(ValueError):
            params.recommend_min_cluster_points(0.2, 0)


if __name__ == "__main__":
    unittest.main()
