import unittest
from casinobot.hypervectors import symbol, bind, unbind, bundle, hamming_distance, similarity, nearest

D = 256

class HypervectorsTests(unittest.TestCase):
    def test_deterministic_symbol(self):
        self.assertEqual(symbol("rtp", dimension=D), symbol("rtp", dimension=D))

    def test_binding_is_reversible(self):
        a, b = symbol("a", dimension=D), symbol("b", dimension=D)
        self.assertEqual(unbind(bind(a, b, dimension=D), b, dimension=D), a)

    def test_hamming(self):
        self.assertEqual(hamming_distance(0, 255, dimension=D), 8)
        self.assertEqual(similarity(0, 0, dimension=D), 1)

    def test_majority(self):
        self.assertEqual(bundle([0, 0, 255], dimension=D), 0)
        self.assertEqual(bundle([255, 255, 0], dimension=D), 255)

    def test_retrieval(self):
        a, b = symbol("a", dimension=D), symbol("b", dimension=D)
        self.assertEqual(nearest(a, {"b": b, "a": a}, dimension=D)[0][0], "a")

    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):
            symbol("x", dimension=8)

if __name__ == "__main__":
    unittest.main()
