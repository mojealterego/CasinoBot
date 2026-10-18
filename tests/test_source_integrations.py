import unittest
from casinobot.lottery_audit import hypergeometric_probability, exact_combination_count, uniformity_statistic
from casinobot.fairness import server_seed_commitment, derive_digest, verify_disclosed_round

class SourceIntegrationTests(unittest.TestCase):
    def test_combinations(self):
        self.assertEqual(exact_combination_count(49, 6), 13983816)

    def test_distribution(self):
        self.assertAlmostEqual(sum(hypergeometric_probability(49, 6, 6, i) for i in range(7)), 1)

    def test_uniformity(self):
        self.assertEqual(uniformity_statistic([0, 1] * 10, 2)["chi_square"], 0)

    def test_commitment(self):
        s, c = "secret", "client"
        h = server_seed_commitment(s)
        d = derive_digest(s, c, 2)
        self.assertTrue(verify_disclosed_round(s, h, c, 2, d))
        self.assertFalse(verify_disclosed_round(s, h, c, 3, d))

if __name__ == "__main__":
    unittest.main()
