"""Regression checks for paired synthetic experiments."""
import unittest
from casinobot.paired import Policy, compare_policies


class PairedTests(unittest.TestCase):
    def test_identical_policies_have_zero_difference(self):
        p = Policy("same", 100, 50)
        r = compare_policies(p, p, sessions=40, seed=7)
        self.assertEqual(r["paired_mean_difference_cents"], 0)
        self.assertEqual(r["paired_difference_ci95_cents"], [0, 0])

    def test_reproducible(self):
        a, b = Policy("a", 100), Policy("b", 200)
        self.assertEqual(compare_policies(a, b, sessions=40, seed=8),
                         compare_policies(a, b, sessions=40, seed=8))

    def test_zero_rounds(self):
        a, b = Policy("a", 100, 0), Policy("b", 200, 0)
        self.assertEqual(compare_policies(a, b, sessions=3)["mean_net_a_cents"], 0)

    def test_bad_sessions(self):
        with self.assertRaises(ValueError):
            compare_policies(Policy("a", 100), Policy("b", 200), sessions=1)


if __name__ == "__main__":
    unittest.main()
