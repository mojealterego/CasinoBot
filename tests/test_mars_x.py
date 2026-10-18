"""Regression tests for MARS-X bounded offline search."""
import unittest
from fractions import Fraction
from casinobot.mars_x import Hypothesis, cognitive_firewall, evaluate, evolve_hypotheses


class MarsXTests(unittest.TestCase):
    def test_invalid_denominator(self):
        with self.assertRaises(ValueError):
            Hypothesis(1, 0)

    def test_firewall(self):
        self.assertFalse(cognitive_firewall(Hypothesis(11, 1))[0])
        self.assertTrue(cognitive_firewall(Hypothesis(1, 2))[0])

    def test_exact_hypothesis_best(self):
        r = evolve_hypotheses(Hypothesis(1, 2), [100] * 4, [50] * 4,
                              generations=2)
        self.assertEqual(r["best"].rtp, Fraction(1, 2))

    def test_determinism(self):
        args = (Hypothesis(1, 2), [100, 100], [50, 100])
        self.assertEqual(evolve_hypotheses(*args), evolve_hypotheses(*args))

    def test_bad_observations(self):
        with self.assertRaises(ValueError):
            evaluate(Hypothesis(1, 2), [100], [1, 2])


if __name__ == "__main__":
    unittest.main()
