import tempfile
import unittest
from pathlib import Path
from casinobot.lotto_csv_audit import compare_archives, load_draws

class LottoCSVAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.a = Path(self.temp.name) / "a.csv"
        self.b = Path(self.temp.name) / "b.csv"
        self.a.write_text("1,01.01.2020,1,2,3,4,5,6\n2,02.01.2020,2,3,4,5,6,7\n")
        self.b.write_text("1,01.01.2020,6,5,4,3,2,1\n2,02.01.2020,7,6,5,4,3,2\n")

    def test_order_independent(self):
        self.assertEqual(compare_archives(self.a, self.b)["integrity_status"], "consistent")

    def test_number_mismatch(self):
        self.b.write_text("1,01.01.2020,1,2,3,4,5,7\n2,02.01.2020,2,3,4,5,6,7\n")
        self.assertEqual(compare_archives(self.a, self.b)["mismatches"][0]["draw_id"], 1)

    def test_date_mismatch(self):
        self.b.write_text("1,02.01.2020,1,2,3,4,5,6\n2,02.01.2020,2,3,4,5,6,7\n")
        self.assertEqual(len(compare_archives(self.a, self.b)["mismatches"]), 1)

    def test_duplicate_numbers_rejected(self):
        self.a.write_text("1,01.01.2020,1,1,3,4,5,6\n")
        with self.assertRaises(ValueError):
            load_draws(self.a)

    def test_missing_id_rejected(self):
        self.a.write_text("1,01.01.2020,1,2,3,4,5,6\n3,02.01.2020,2,3,4,5,6,7\n")
        with self.assertRaises(ValueError):
            load_draws(self.a)

    def test_empty_rejected(self):
        self.a.write_text("")
        with self.assertRaises(ValueError):
            load_draws(self.a)

    def test_ragged_rejected(self):
        self.a.write_text("1,01.01.2020,1,2\n")
        with self.assertRaises(ValueError):
            load_draws(self.a)

if __name__ == "__main__":
    unittest.main()
