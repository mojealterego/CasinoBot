"""Regression tests for bootstrap and payout concentration."""
import unittest
from casinobot.bootstrap import bootstrap_rtp, tail_diagnostics


class BootstrapTests(unittest.TestCase):
    def test_constant_return(self):
        r = bootstrap_rtp([100] * 20, [90] * 20, resamples=100, seed=7)
        self.assertEqual(r["percentile_ci"], [0.9, 0.9])

    def test_deterministic(self):
        args = dict(resamples=150, seed=17)
        self.assertEqual(
            bootstrap_rtp([100] * 5, [0, 0, 100, 200, 0], **args),
            bootstrap_rtp([100] * 5, [0, 0, 100, 200, 0], **args),
        )

    def test_variable_stakes(self):
        r = bootstrap_rtp([100, 200], [50, 100], resamples=100)
        self.assertAlmostEqual(r["empirical_rtp"], 0.5)

    def test_invalid_resamples(self):
        with self.assertRaises(ValueError):
            bootstrap_rtp([100], [1], resamples=99)

    def test_tail_concentration(self):
        r = tail_diagnostics([0] * 99 + [1000])
        self.assertEqual(r["top_one_percent_share_of_payouts"], 1.0)
        self.assertEqual(r["zero_payout_fraction"], 0.99)

    def test_zero_total(self):
        self.assertIsNone(tail_diagnostics([0, 0])["top_one_percent_share_of_payouts"])


if __name__ == "__main__":
    unittest.main()
