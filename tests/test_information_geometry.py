import math
import unittest

from casinobot.information_geometry import (
    bernoulli_kl, fisher_information_bernoulli,
    fisher_rao_distance_bernoulli, local_kl_quadratic,
)


class InformationGeometryTests(unittest.TestCase):
    def test_fisher_at_half(self):
        self.assertAlmostEqual(fisher_information_bernoulli(0.5), 4.0)

    def test_kl_identity(self):
        self.assertAlmostEqual(bernoulli_kl(0.3, 0.3), 0.0)

    def test_kl_asymmetric(self):
        self.assertNotAlmostEqual(bernoulli_kl(0.2, 0.5), bernoulli_kl(0.5, 0.2))

    def test_distance_symmetric(self):
        self.assertAlmostEqual(fisher_rao_distance_bernoulli(0.2, 0.8),
                               fisher_rao_distance_bernoulli(0.8, 0.2))

    def test_distance_zero(self):
        self.assertAlmostEqual(fisher_rao_distance_bernoulli(0.4, 0.4), 0.0)

    def test_local_kl_approximation(self):
        actual = bernoulli_kl(0.4, 0.40001)
        approx = local_kl_quadratic(0.4, 0.00001)
        self.assertAlmostEqual(actual / approx, 1.0, places=3)

    def test_reject_boundary(self):
        for p in (0, 1, float("nan"), float("inf"), -0.1):
            with self.subTest(p=p), self.assertRaises(ValueError):
                fisher_information_bernoulli(p)

    def test_reject_invalid_shift(self):
        with self.assertRaises(ValueError):
            local_kl_quadratic(0.9, 0.2)


if __name__ == "__main__":
    unittest.main()
