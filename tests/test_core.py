import unittest
from decimal import Decimal
from casinobot import Config, simulate

class TestSimulator(unittest.TestCase):
    def test_determinism(self):
        cfg = Config(seed=17)
        self.assertEqual(simulate(cfg), simulate(cfg))

    def test_conservation(self):
        cfg = Config()
        result = simulate(cfg)
        self.assertEqual(result.final_credits, cfg.starting_credits - result.total_staked + result.total_paid)

    def test_zero_probability(self):
        result = simulate(Config(starting_credits=Decimal("3"), payout_probability=0))
        self.assertEqual(result.rounds, 3)
        self.assertEqual(result.final_credits, 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Config(stake=Decimal("0"))

    def test_no_negative_balance(self):
        result = simulate(Config(starting_credits=Decimal("2"), stake=Decimal("3")))
        self.assertEqual(result.rounds, 0)
        self.assertEqual(result.final_credits, 2)

if __name__ == "__main__":
    unittest.main()
