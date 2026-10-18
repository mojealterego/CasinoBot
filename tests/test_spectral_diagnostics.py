import unittest
from math import sqrt
from casinobot.spectral_diagnostics import symmetric_eigen, symmetric_rank_k

class SpectralTests(unittest.TestCase):
    def test_diagonal(self):
        values, vectors = symmetric_eigen([[2, 0], [0, 5]])
        self.assertEqual(values, [5, 2])
        self.assertAlmostEqual(sum(vectors[i][0] ** 2 for i in range(2)), 1)

    def test_nondiagonal(self):
        values, vectors = symmetric_eigen([[2, 1], [1, 2]])
        self.assertAlmostEqual(values[0], 3)
        self.assertAlmostEqual(values[1], 1)
        for k in range(2):
            for i in range(2):
                lhs = sum([[2, 1], [1, 2]][i][j] * vectors[j][k] for j in range(2))
                self.assertAlmostEqual(lhs, values[k] * vectors[i][k])

    def test_rank_full(self):
        self.assertAlmostEqual(symmetric_rank_k([[2, 1], [1, 2]], 2)["frobenius_error"], 0, places=8)

    def test_rank_zero(self):
        self.assertAlmostEqual(symmetric_rank_k([[3, 0], [0, 4]], 0)["frobenius_error"], 5)

    def test_rank_one(self):
        self.assertAlmostEqual(symmetric_rank_k([[3, 0], [0, 4]], 1)["frobenius_error"], 3)

    def test_reject_asymmetric(self):
        with self.assertRaises(ValueError):
            symmetric_eigen([[1, 2], [0, 1]])

    def test_reject_nonfinite(self):
        with self.assertRaises(ValueError):
            symmetric_eigen([[float("inf")]])

    def test_reject_invalid_rank(self):
        with self.assertRaises(ValueError):
            symmetric_rank_k([[1]], 2)

if __name__ == "__main__":
    unittest.main()
