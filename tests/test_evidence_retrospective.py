import unittest
from casinobot.evidence_reasoning import judgment, revise, expected_support, conflicting_evidence
from casinobot.retrospective import retrospective_penalties, penalty_lookup

class EvidenceTests(unittest.TestCase):
    def test_no_evidence(self):
        self.assertEqual(judgment(0, 0).frequency, 0.5)
        self.assertEqual(judgment(0, 0).confidence, 0)

    def test_conflicting(self):
        self.assertTrue(conflicting_evidence(judgment(9, 1), judgment(1, 9)))

    def test_independent_revision(self):
        self.assertEqual(revise(judgment(2, 1), judgment(1, 2),
                                independent=True).frequency, 0.5)

    def test_reject_double_count(self):
        with self.assertRaises(ValueError):
            revise(judgment(1, 0), judgment(1, 0), independent=False)

    def test_expectation(self):
        self.assertAlmostEqual(expected_support(judgment(1, 0)), 2/3)

class RetrospectiveTests(unittest.TestCase):
    def test_decay(self):
        penalties = retrospective_penalties(["a", "b", "c"], failure_index=2)
        self.assertEqual([p["penalty"] for p in penalties], [0.25, 0.5, 1.0])

    def test_aggregate_repeated(self):
        result = penalty_lookup(retrospective_penalties(["a", "a"], failure_index=1))
        self.assertEqual(result["a"], 1.5)

    def test_invalid_index(self):
        with self.assertRaises(ValueError):
            retrospective_penalties(["a"], failure_index=1)

if __name__ == "__main__":
    unittest.main()
