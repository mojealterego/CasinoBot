import unittest
from casinobot.matrix_decompositions import cholesky, covariance

class MatrixDecompositionTests(unittest.TestCase):
    def test_spd(self):
        l = cholesky([[4, 2], [2, 3]])
        self.assertAlmostEqual(l[0][0], 2)
        self.assertAlmostEqual(l[1][0], 1)
        self.assertAlmostEqual(l[1][1] ** 2, 2)

    def test_identity(self):
        self.assertEqual(cholesky([[1, 0], [0, 1]]), [[1.0, 0.0], [0.0, 1.0]])

    def test_non_symmetric(self):
        with self.assertRaises(ValueError):
            cholesky([[1, 2], [0, 1]])

    def test_semidefinite(self):
        with self.assertRaises(ValueError):
            cholesky([[1, 1], [1, 1]])

    def test_negative_diagonal(self):
        with self.assertRaises(ValueError):
            cholesky([[-1]])

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            cholesky([[float("nan")]])

    def test_covariance(self):
        self.assertEqual(covariance([[1, 2], [3, 4], [5, 6]]),
                         [[4.0, 4.0], [4.0, 4.0]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            covariance([[1, 2], [3]])

if __name__ == "__main__":
    unittest.main()
