import unittest
from casinobot.engine import SessionConfig, run_session, run_experiment
from casinobot.model import PayoutModel

class TestEngine(unittest.TestCase):
    def test_reproducible(self):
        a = run_session(SessionConfig(), PayoutModel(), 42)
        self.assertEqual(a, run_session(SessionConfig(), PayoutModel(), 42))

    def test_accounting(self):
        result = run_session(SessionConfig(), PayoutModel(), 5)
        self.assertEqual(result.final_cents, result.initial_cents - result.wagered_cents + result.paid_cents)

    def test_zero_rtp(self):
        result = run_session(SessionConfig(max_rounds=100), PayoutModel(0), 1)
        self.assertEqual(result.paid_cents, 0)
        self.assertGreaterEqual(result.final_cents, 16000)

    def test_no_stake_beyond_floor(self):
        result = run_session(SessionConfig(max_loss_cents=0), PayoutModel(), 1)
        self.assertEqual(result.rounds, 0)

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            SessionConfig(stake_cents=0)
        with self.assertRaises(ValueError):
            PayoutModel(10001)
        with self.assertRaises(ValueError):
            run_experiment(SessionConfig(), PayoutModel(), 0, 1)

    def test_rtp_approximation(self):
        result = run_experiment(SessionConfig(max_rounds=1, max_loss_cents=20000), PayoutModel(), 100000, 42)
        self.assertAlmostEqual(result["empirical_rtp_percent"], 96.59, delta=2.0)

if __name__ == "__main__":
    unittest.main()
