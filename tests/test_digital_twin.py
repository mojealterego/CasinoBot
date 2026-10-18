import unittest
from casinobot.digital_twin import simulate, compare_candidate

class DigitalTwinTests(unittest.TestCase):
    def test_within_capacity(self):
        result = simulate([(0, 2), (1, -1)], initial_capacity=3)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["load"], 1)

    def test_overload(self):
        result = simulate([(0, 3), (1, 2)], initial_capacity=4)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["time"], 1)

    def test_underflow(self):
        self.assertEqual(simulate([(0, -1)])["status"], "rejected")

    def test_stable_equal_time_order(self):
        self.assertEqual(simulate([(1, 1), (1, -1)], initial_capacity=1)["status"], "accepted")

    def test_candidate_gate(self):
        result = compare_candidate([(0, 1)], [(0, 5)], capacity=2)
        self.assertFalse(result["promotion_eligible"])

    def test_event_budget(self):
        with self.assertRaises(ValueError):
            simulate([(0, 1), (1, -1)], max_events=1)

if __name__ == "__main__":
    unittest.main()
