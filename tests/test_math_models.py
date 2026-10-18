"""Tests of offline mathematical model primitives."""
import unittest
from casinobot.math_models import (
    bezier_point, fitts_movement_time, shannon_entropy,
    ltn_satisfaction, compute_roi,
)


class MathModelTests(unittest.TestCase):
    def test_bezier_endpoints(self):
        points = [(0., 0.), (1., 3.), (2., 0.)]
        self.assertEqual(bezier_point(points, 0), (0., 0.))
        self.assertEqual(bezier_point(points, 1), (2., 0.))

    def test_bezier_midpoint(self):
        self.assertEqual(bezier_point([(0., 0.), (2., 2.)], 0.5), (1., 1.))

    def test_fitts(self):
        self.assertAlmostEqual(fitts_movement_time(3, 1, 0.2, 0.5), 1.2)

    def test_entropy(self):
        self.assertAlmostEqual(shannon_entropy([0.5, 0.5]), 1)
        self.assertEqual(shannon_entropy([1, 0]), 0)

    def test_ltn_aggregation(self):
        self.assertAlmostEqual(ltn_satisfaction([1, 0.5, 0]), 0.5)

    def test_roi(self):
        self.assertAlmostEqual(compute_roi(150, 100), 0.5)

    def test_invalid_distribution(self):
        with self.assertRaises(ValueError):
            shannon_entropy([0.2, 0.2])


if __name__ == "__main__":
    unittest.main()
