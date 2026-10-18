import unittest
from casinobot.geometry_benchmark import bernoulli_calibration


class GeometryBenchmarkTests(unittest.TestCase):
    def test_reproducibility(self):
        self.assertEqual(bernoulli_calibration(samples=500, seed=7),
                         bernoulli_calibration(samples=500, seed=7))

    def test_existing_kl_agrees(self):
        self.assertLess(bernoulli_calibration()["kl_consistency_error"], 1e-12)

    def test_identity(self):
        result = bernoulli_calibration(p=0.5, q=0.5, samples=200)
        self.assertAlmostEqual(result["bernoulli_kl"], 0)
        self.assertAlmostEqual(result["fisher_rao_distance"], 0)

    def test_empirical_boundary_zero(self):
        result = bernoulli_calibration(p=0.00000001, q=0.2, samples=2, seed=1)
        self.assertEqual(result["empirical_p"], 0.0)
        self.assertGreater(result["empirical_kl"], 0)

    def test_invalid_sample_count(self):
        for value in (0, 1, True, 1.5, 1000001):
            with self.subTest(value=value), self.assertRaises(ValueError):
                bernoulli_calibration(samples=value)

    def test_invalid_probabilities(self):
        for p, q in ((0, 0.5), (0.5, 1), (float("nan"), 0.3)):
            with self.subTest(p=p, q=q), self.assertRaises(ValueError):
                bernoulli_calibration(p=p, q=q)

    def test_empirical_rate_range(self):
        result = bernoulli_calibration(samples=1000)
        self.assertGreaterEqual(result["empirical_p"], 0)
        self.assertLessEqual(result["empirical_p"], 1)


if __name__ == "__main__":
    unittest.main()
