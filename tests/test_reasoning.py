"""Tests of exact mathematical reasoning and bounded falsification."""
import unittest
from fractions import Fraction as F
from casinobot.reasoning import (
    Outcome, exact_game_analysis, falsify_claim,
    verify_distribution, verify_nonpositive_expected_profit,
)


class ReasoningTests(unittest.TestCase):
    def setUp(self):
        self.model = [Outcome("loss", F(3, 4), F(0)),
                      Outcome("win", F(1, 4), F(3))]

    def test_exact_rtp(self):
        result = exact_game_analysis(self.model)
        self.assertEqual(result["rtp"], F(3, 4))
        self.assertEqual(result["house_edge"], F(1, 4))
        self.assertEqual(result["hit_probability"], F(1, 4))
        self.assertEqual(result["variance"], F(27, 16))

    def test_probability_normalization(self):
        with self.assertRaises(ValueError):
            verify_distribution([Outcome("a", F(1, 3), F(2))])

    def test_duplicate_labels(self):
        with self.assertRaises(ValueError):
            verify_distribution([Outcome("a", F(1, 2), F(0)),
                                 Outcome("a", F(1, 2), F(1))])

    def test_shortest_counterexample(self):
        result = falsify_claim(self.model, lambda seq: all(x <= 2 for x in seq))
        self.assertEqual(result["counterexample"], (F(3),))
        self.assertEqual(result["depth"], 1)

    def test_bounded_no_counterexample(self):
        self.assertIsNone(falsify_claim(self.model, lambda seq: all(x >= 0 for x in seq)))

    def test_expected_profit(self):
        result = verify_nonpositive_expected_profit(self.model, rounds=8)
        self.assertEqual(result["expected_net"], F(-2))
        self.assertTrue(result["nonpositive"])

    def test_zero_probability_not_enumerated(self):
        model = [Outcome("safe", F(1), F(0)),
                 Outcome("impossible", F(0), F(100))]
        self.assertIsNone(falsify_claim(model, lambda seq: all(x < 100 for x in seq)))


if __name__ == "__main__":
    unittest.main()
