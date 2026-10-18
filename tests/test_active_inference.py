import unittest
from casinobot.active_inference import posterior, evaluate_experiment, rank_experiments

class ActiveInferenceTests(unittest.TestCase):
    def test_bayesian_update(self):
        self.assertEqual(posterior([0.5, 0.5], [[0.9, 0.1], [0.1, 0.9]], 0),
                         (0.9, 0.1))

    def test_perfect_sensor(self):
        result = evaluate_experiment([0.5, 0.5], [[1, 0], [0, 1]], [0.5, 0.5])
        self.assertAlmostEqual(result["risk_kl"], 0)
        self.assertAlmostEqual(result["ambiguity"], 0)
        self.assertAlmostEqual(result["information_gain"], 0.6931471805599453)

    def test_uninformative_sensor(self):
        result = evaluate_experiment([0.5, 0.5], [[0.5, 0.5], [0.5, 0.5]], [0.5, 0.5])
        self.assertAlmostEqual(result["information_gain"], 0)

    def test_experiment_ranking(self):
        models = {"uninformative": [[0.5, 0.5], [0.5, 0.5]],
                  "informative": [[1, 0], [0, 1]]}
        results = rank_experiments([0.5, 0.5], models, [0.5, 0.5])
        self.assertEqual(results[0]["experiment"], "informative")

    def test_zero_evidence(self):
        with self.assertRaises(ValueError):
            posterior([1, 0], [[0, 1], [1, 0]], 0)

    def test_bad_distribution(self):
        with self.assertRaises(ValueError):
            evaluate_experiment([0.6, 0.6], [[1, 0], [0, 1]], [0.5, 0.5])

if __name__ == "__main__":
    unittest.main()
