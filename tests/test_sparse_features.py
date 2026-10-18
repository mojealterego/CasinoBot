import unittest
from casinobot.sparse_features import sparse_encode, reconstruction_metrics

class SparseFeaturesTests(unittest.TestCase):
    def test_identity_dictionary(self):
        x = [[1.0, 0.0], [0.0, 1.0]]
        d = [[1.0, 0.0], [0.0, 1.0]]
        codes = sparse_encode(x, d, l1=0.0, steps=250, rate=0.1)
        metrics = reconstruction_metrics(x, d, codes)
        self.assertLess(metrics["mse"], 1e-6)
        self.assertEqual(metrics["samples"], 2)

    def test_l1_reduces_activation(self):
        x, d = [[1.0]], [[1.0]]
        sparse = sparse_encode(x, d, l1=0.5, steps=200, rate=0.1)
        dense = sparse_encode(x, d, l1=0, steps=200, rate=0.1)
        self.assertLess(sparse[0][0], dense[0][0])

    def test_bad_dimensions(self):
        with self.assertRaises(ValueError):
            sparse_encode([[1, 2]], [[1]])

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            sparse_encode([[float("nan")]], [[1]])

if __name__ == "__main__":
    unittest.main()
