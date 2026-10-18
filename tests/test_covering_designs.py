import unittest
from itertools import combinations
from casinobot.covering_designs import verify_covering

class CoveringDesignTests(unittest.TestCase):
    def test_full_system(self):
        r = verify_covering(7, 6, 3, list(combinations(range(1, 8), 6)))
        self.assertTrue(r["guaranteed"])
        self.assertEqual(r["covered_subsets"], 35)

    def test_partial(self):
        r = verify_covering(7, 6, 3, [(1, 2, 3, 4, 5, 6)])
        self.assertFalse(r["guaranteed"])
        self.assertEqual(r["covered_subsets"], 20)
        self.assertIsNotNone(r["first_uncovered"])

    def test_one_block_exact(self):
        self.assertTrue(verify_covering(6, 6, 3, [(1, 2, 3, 4, 5, 6)])["guaranteed"])

    def test_duplicate_block(self):
        b = (1, 2, 3, 4, 5, 6)
        with self.assertRaises(ValueError):
            verify_covering(7, 6, 3, [b, b])

    def test_duplicate_position(self):
        with self.assertRaises(ValueError):
            verify_covering(7, 6, 3, [(1, 1, 2, 3, 4, 5)])

    def test_invalid_parameter(self):
        with self.assertRaises(ValueError):
            verify_covering(6, 3, 4, [(1, 2, 3)])

    def test_bounded(self):
        with self.assertRaises(ValueError):
            verify_covering(49, 6, 3, [(1, 2, 3, 4, 5, 6)], max_subsets=100)

if __name__ == "__main__":
    unittest.main()
