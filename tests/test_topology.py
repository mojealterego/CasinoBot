import unittest
from casinobot.topology import vietoris_rips_betti, radius_scan

class TopologyTests(unittest.TestCase):
    def test_disconnected(self):
        self.assertEqual(vietoris_rips_betti([(0, 0), (3, 0)], 1)["betti"], [2, 0, 0])

    def test_connected_segment(self):
        self.assertEqual(vietoris_rips_betti([(0, 0), (1, 0)], 1)["betti"], [1, 0, 0])

    def test_square_cycle(self):
        self.assertEqual(vietoris_rips_betti([(0, 0), (1, 0), (1, 1), (0, 1)], 1.01)["betti"], [1, 1, 0])

    def test_filled_triangle(self):
        self.assertEqual(vietoris_rips_betti([(0, 0), (1, 0), (0.5, 0.8)], 1.01)["betti"], [1, 0, 0])

    def test_tetrahedral_shell(self):
        # Four vertices alone produce a filled 3-simplex, not a 2D cavity.
        pts = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.assertEqual(vietoris_rips_betti(pts, 1.5)["betti"], [1, 0, 0])

    def test_scan(self):
        self.assertEqual(len(radius_scan([(0,), (1,)], [0, 1])), 2)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            vietoris_rips_betti([(0,), (1, 2)], 1)
        with self.assertRaises(ValueError):
            radius_scan([(0,), (1,)], [1, 0])

if __name__ == "__main__":
    unittest.main()
