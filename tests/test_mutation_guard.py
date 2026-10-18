import unittest
from casinobot.mutation_guard import verify_transition_system

class MutationGuardTests(unittest.TestCase):
    def test_safe_acyclic(self):
        result = verify_transition_system("start", {"start": ["end"]}, require_termination=True)
        self.assertEqual(result["status"], "accepted")

    def test_forbidden_counterexample(self):
        result = verify_transition_system("start", {"start": ["bad"]}, forbidden=["bad"])
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["counterexample"], ["start", "bad"])

    def test_cycle(self):
        result = verify_transition_system("a", {"a": ["b"], "b": ["a"]},
                                          require_termination=True)
        self.assertEqual(result["reason"], "reachable_cycle")

    def test_depth_inconclusive(self):
        result = verify_transition_system("a", {"a": ["b"], "b": ["c"]}, max_depth=1)
        self.assertEqual(result["status"], "inconclusive")

    def test_invalid_successors(self):
        with self.assertRaises(ValueError):
            verify_transition_system("a", {"a": "b"})

if __name__ == "__main__":
    unittest.main()
