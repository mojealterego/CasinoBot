import tempfile
import unittest
from math import comb
from pathlib import Path
from casinobot.covering_import import full_system, import_blocks

class CoveringImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "system.csv"

    def test_full_system(self):
        blocks = full_system(7, 6)
        self.assertEqual(len(blocks), 7)
        self.assertEqual(blocks[0], (1, 2, 3, 4, 5, 6))

    def test_full_system_limit(self):
        with self.assertRaises(ValueError):
            full_system(12, 6, max_blocks=100)

    def test_import_header(self):
        self.path.write_text("L1,L2,L3\n1,2,3\n1,2,4\n1,3,4\n2,3,4\n")
        self.assertTrue(import_blocks(self.path, v=4, k=3, t=2)["guaranteed"])

    def test_import_no_header(self):
        self.path.write_text("1,2,3\n")
        self.assertFalse(import_blocks(self.path, v=4, k=3, t=2)["guaranteed"])

    def test_duplicate_in_ticket(self):
        self.path.write_text("1,1,3\n")
        with self.assertRaises(ValueError):
            import_blocks(self.path, v=4, k=3, t=2)

    def test_duplicate_ticket(self):
        self.path.write_text("1,2,3\n3,2,1\n")
        with self.assertRaises(ValueError):
            import_blocks(self.path, v=4, k=3, t=2)

    def test_bad_csv(self):
        self.path.write_text("1,2\n")
        with self.assertRaises(ValueError):
            import_blocks(self.path, v=4, k=3, t=2)

    def test_row_limit(self):
        self.path.write_text("1,2,3\n1,2,4\n")
        with self.assertRaises(ValueError):
            import_blocks(self.path, v=4, k=3, t=2, max_rows=1)

if __name__ == "__main__":
    unittest.main()
