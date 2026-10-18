import unittest
from copy import deepcopy
from casinobot.proof_receipts import make_receipt, verify_receipt

class ProofReceiptTests(unittest.TestCase):
    def test_sum(self):
        self.assertTrue(verify_receipt(make_receipt("sum", [2, 3, -1])))

    def test_product(self):
        self.assertEqual(make_receipt("product", [2, 3, 4])["statement"]["result"], 24)

    def test_squares(self):
        self.assertEqual(make_receipt("sum_of_squares", [3, 4])["statement"]["result"], 25)

    def test_tamper_result(self):
        receipt = make_receipt("sum", [1, 2])
        receipt["statement"]["result"] = 99
        self.assertFalse(verify_receipt(receipt))

    def test_tamper_input(self):
        receipt = make_receipt("sum", [1, 2])
        receipt["statement"]["inputs"][0] = 100
        self.assertFalse(verify_receipt(receipt))

    def test_invalid_operation(self):
        with self.assertRaises(ValueError):
            make_receipt("eval", [1])

    def test_reject_extra_field(self):
        receipt = make_receipt("sum", [1])
        receipt["untrusted"] = True
        self.assertFalse(verify_receipt(receipt))

if __name__ == "__main__":
    unittest.main()
