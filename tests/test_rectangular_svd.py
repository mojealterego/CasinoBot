import unittest
from casinobot.rectangular_svd import truncated_svd

class RectangularSVDTests(unittest.TestCase):
    def test_tall_rank_one(self):
        r = truncated_svd([[3, 0], [4, 0], [0, 0]], 1)
        self.assertAlmostEqual(r["singular_values"][0], 5)
        self.assertAlmostEqual(r["frobenius_error"], 0)

    def test_wide(self):
        r = truncated_svd([[3, 0, 0], [0, 4, 0]], 1)
        self.assertAlmostEqual(r["frobenius_error"], 3)
        self.assertEqual(r["shape"], [2, 3])

    def test_full_reconstruction(self):
        self.assertLess(truncated_svd([[1, 2], [3, 4], [5, 6]])["frobenius_error"], 1e-7)

    def test_zero_matrix(self):
        self.assertEqual(truncated_svd([[0, 0, 0]], 1)["frobenius_error"], 0)

    def test_zero_rank(self):
        self.assertAlmostEqual(truncated_svd([[3, 4]], 0)["frobenius_error"], 5)

    def test_invalid_rank(self):
        with self.assertRaises(ValueError):
            truncated_svd([[1, 2]], 2)

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            truncated_svd([[float("nan")]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            truncated_svd([[1], [1, 2]])

    def test_nonsymmetric_input(self):
        self.assertLess(truncated_svd([[1, 2], [3, 4]], 2)["frobenius_error"], 1e-7)

if __name__ == "__main__":
    unittest.main()
