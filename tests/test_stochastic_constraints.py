import unittest
from fractions import Fraction as F
from casinobot.stochastic_constraints import weighted_model_count as w

class WeightedCountTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(w([],[])['probability'],1)
    def test_false_clause(self): self.assertEqual(w([F(1,2)],[[]])['probability'],0)
    def test_literal(self): self.assertEqual(w([F(1,3)],[[1]])['probability'],F(1,3))
    def test_negative_literal(self): self.assertEqual(w([F(1,3)],[[-1]])['probability'],F(2,3))
    def test_and(self): self.assertEqual(w([F(1,2),F(1,4)],[[1],[2]])['probability'],F(1,8))
    def test_or(self): self.assertEqual(w([F(1,2),F(1,4)],[[1,2]])['probability'],F(5,8))
    def test_contradiction(self): self.assertEqual(w([F(1,2)],[[1],[-1]])['probability'],0)
    def test_zero_probability(self): self.assertEqual(w([F(0)],[[1]])['probability'],0)
    def test_limit(self):
        with self.assertRaises(ValueError): w([F(1,2)]*17,[])
    def test_bad_literal(self):
        with self.assertRaises(ValueError): w([F(1,2)],[[2]])
    def test_reject_float(self):
        with self.assertRaises(ValueError): w([0.5],[[1]])
    def test_reject_bool_literal(self):
        with self.assertRaises(ValueError): w([F(1,2)],[[True]])

if __name__=='__main__': unittest.main()
