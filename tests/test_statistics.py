"""Tests for source-inspired statistical diagnostics."""
import math
import unittest
from casinobot.statistics import payout_statistics, kl_divergence, wasserstein_1_discrete


class StatisticsTests(unittest.TestCase):
    def test_accounting_rtp(self):
        x = payout_statistics([100] * 4, [0, 100, 200, 100])
        self.assertAlmostEqual(x["empirical_rtp"], 1.0)
        self.assertAlmostEqual(x["mean_net_cents_per_round"], 0)
        self.assertIsNotNone(x["rtp_confidence_interval"])

    def test_single_observation_has_no_ci(self):
        self.assertIsNone(payout_statistics([100], [200])["rtp_confidence_interval"])

    def test_invalid_stakes(self):
        with self.assertRaises(ValueError):
            payout_statistics([100, 200], [100, 200])

    def test_kl_identical(self):
        self.assertAlmostEqual(kl_divergence([0.2, 0.8], [0.2, 0.8]), 0)

    def test_kl_zero_support(self):
        self.assertTrue(math.isinf(kl_divergence([1, 0], [0, 1])))

    def test_wasserstein(self):
        self.assertAlmostEqual(wasserstein_1_discrete([1, 0], [0, 1], [0, 3]), 3)

    def test_wasserstein_identical(self):
        self.assertAlmostEqual(wasserstein_1_discrete([0.2, 0.8], [0.2, 0.8], [0, 3]), 0)


if __name__ == "__main__":
    unittest.main()
