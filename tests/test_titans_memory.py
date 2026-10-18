"""Tests for surprise memory diagnostics."""
import math
import unittest
from casinobot.titans_memory import SurpriseMemory


class SurpriseMemoryTests(unittest.TestCase):
    def test_surprise(self):
        m = SurpriseMemory()
        x = m.observe(0.25)
        self.assertAlmostEqual(x["surprise"], math.log(4))

    def test_gate_bounds(self):
        m = SurpriseMemory(decay=0.8)
        for p in [1, 0.5, 1e-100]:
            x = m.observe(p)
            self.assertGreaterEqual(x["weight_decay_gate"], 0.8)
            self.assertLessEqual(x["weight_decay_gate"], 1)

    def test_reproducible(self):
        a, b = SurpriseMemory(), SurpriseMemory()
        for p in [0.1, 0.9, 0.4]:
            self.assertEqual(a.observe(p), b.observe(p))

    def test_invalid_probability(self):
        m = SurpriseMemory()
        for p in [0, -1, 1.1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                m.observe(p)

    def test_reset(self):
        m = SurpriseMemory()
        m.observe(0.2)
        m.reset()
        self.assertEqual(m.state.observations, 0)


if __name__ == "__main__":
    unittest.main()
