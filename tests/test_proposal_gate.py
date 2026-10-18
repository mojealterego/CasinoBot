import unittest

from casinobot.evidence_reasoning import judgment
from casinobot.proposal_gate import evaluate_proposal


def check(**overrides):
    args = dict(
        proposal_id="candidate",
        initial_state="start",
        transitions={"start": ["done"], "done": []},
        baseline_events=[(0, 1), (1, -1)],
        candidate_events=[(0, 2), (1, -1)],
        capacity=3,
        evidence=judgment(9, 1),
    )
    args.update(overrides)
    return evaluate_proposal(**args)


class ProposalGateTests(unittest.TestCase):
    def test_eligible_never_deploys(self):
        result = check()
        self.assertEqual(result["status"], "eligible_for_human_review")
        self.assertFalse(result["deployment_authorized"])
        self.assertTrue(all(result["gates"].values()))

    def test_forbidden_state(self):
        result = check(forbidden=("done",))
        self.assertFalse(result["gates"]["model_checked"])
        self.assertEqual(result["status"], "rejected")

    def test_inconclusive_fails_closed(self):
        result = check(max_depth=0)
        self.assertEqual(result["model"]["status"], "inconclusive")
        self.assertEqual(result["status"], "rejected")

    def test_cycle_rejected(self):
        result = check(transitions={"start": ["start"]})
        self.assertEqual(result["status"], "rejected")

    def test_overcapacity_rejected(self):
        result = check(candidate_events=[(0, 4)])
        self.assertFalse(result["gates"]["digital_twin"])

    def test_weak_evidence_rejected(self):
        result = check(evidence=judgment(0, 0))
        self.assertFalse(result["gates"]["evidence"])

    def test_failure_penalty_rejected(self):
        result = check(history=["candidate"], failure_index=0)
        self.assertEqual(result["penalty"], 1)
        self.assertFalse(result["gates"]["retrospective"])

    def test_no_implicit_failure_history(self):
        with self.assertRaises(ValueError):
            check(history=["candidate"])

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            check(min_support=float("nan"))


if __name__ == "__main__":
    unittest.main()
