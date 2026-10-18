import unittest
from datetime import datetime, timezone, timedelta
from casinobot.annealing import anneal
from casinobot.scenario_memory import ScenarioMemory

T = datetime(2026, 1, 1, tzinfo=timezone.utc)

class AnnealingTests(unittest.TestCase):
    def test_reproducible(self):
        def run():
            return anneal(4, lambda x: (x-2)**2,
                          lambda x, rng: x+rng.choice([-1, 1]),
                          lambda x: 0 <= x <= 5, steps=50, seed=7)
        self.assertEqual(run(), run())

    def test_hard_gate(self):
        result = anneal(0, lambda x: x*x, lambda x, rng: -1,
                        lambda x: x >= 0, steps=5)
        self.assertEqual(result["best"], 0)
        self.assertEqual(result["rejected_invalid"], 5)

    def test_invalid_temperature(self):
        with self.assertRaises(ValueError):
            anneal(0, lambda x: x, lambda x, rng: x, lambda x: True,
                   start_temperature=0)

class ScenarioMemoryTests(unittest.TestCase):
    def test_temporal_cutoff(self):
        memory = ScenarioMemory()
        memory.record("s1", valid_from=T, recorded_at=T+timedelta(days=1),
                      features={"load": 0.9}, response="inspect capacity")
        self.assertEqual(memory.retrieve({"load": 0.9}, valid_at=T+timedelta(days=2),
                         known_at=T), [])
        result = memory.retrieve({"load": 0.9}, valid_at=T+timedelta(days=2),
                                 known_at=T+timedelta(days=2))
        self.assertEqual(result[0]["scenario_id"], "s1")

    def test_nearest_scenario(self):
        memory = ScenarioMemory()
        memory.record("far", valid_from=T, recorded_at=T,
                      features={"load": 0.1}, response="check")
        memory.record("near", valid_from=T, recorded_at=T,
                      features={"load": 0.9}, response="inspect")
        self.assertEqual(memory.retrieve({"load": 0.8}, valid_at=T, known_at=T)[0]["scenario_id"],
                         "near")

    def test_naive_timestamp_rejected(self):
        memory = ScenarioMemory()
        with self.assertRaises(ValueError):
            memory.record("bad", valid_from=datetime(2026, 1, 1), recorded_at=T,
                          features={"x": 1}, response="check")

if __name__ == "__main__":
    unittest.main()
