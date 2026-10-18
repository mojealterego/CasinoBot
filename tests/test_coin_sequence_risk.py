import unittest
from casinobot.coin_sequence_risk import BASES, exposure, expected_net_for_fixed_stakes

class CoinSequenceRiskTests(unittest.TestCase):
    def test_bases_transcribed(self):
        self.assertEqual(BASES["I"], (1, 2, 3, 15, 50, 150, 500))
        self.assertEqual(BASES["II"], (1, 3, 15, 50, 150, 500, 2500))
        self.assertEqual(BASES["III"], (1, 15, 50, 150, 500, 2500, 8000))

    def test_exposure(self):
        self.assertEqual(exposure("I")["worst_case_loss"], 2163)
        self.assertEqual(exposure("II")["worst_case_loss"], 9657)
        self.assertEqual(exposure("III")["worst_case_loss"], 33447)

    def test_bankroll(self):
        self.assertFalse(exposure("III", bankroll=100)["bankroll_sufficient_for_all_losses"])
        self.assertTrue(exposure("I", bankroll=2163)["bankroll_sufficient_for_all_losses"])

    def test_scaling(self):
        self.assertEqual(exposure("I", unit=2, rounds_per_level=2)["worst_case_loss"], 2884)

    def test_expected_net(self):
        self.assertAlmostEqual(expected_net_for_fixed_stakes("I", rtp=0.95), -108.15)

    def test_reject_invalid(self):
        for base in ("IV", "", None):
            with self.assertRaises(ValueError):
                exposure(base)
        for unit in (0, -1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                exposure("I", unit=unit)
        for rounds in (0, 101, 2.5, True):
            with self.assertRaises(ValueError):
                exposure("I", rounds_per_level=rounds)
        for rtp in (-0.1, 1.1, float("nan"), True):
            with self.assertRaises(ValueError):
                expected_net_for_fixed_stakes("I", rtp=rtp)

if __name__ == "__main__":
    unittest.main()
