import csv, os, tempfile, unittest
from row_hash import add_hashes, row_hash

class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.src = os.path.join(self.d, "a.csv")
        with open(self.src, "w", encoding="utf-8") as f:
            f.write("id,name,ts\n1,Ann ,2026-01-01\n2,Bob,2026-01-02\n")
    def read(self, p):
        with open(p, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    def test_stable_and_trimmed(self):
        self.assertEqual(row_hash({"a": " x "}, ["a"]), row_hash({"a": "x"}, ["a"]))
    def test_subset_ignores_other_cols(self):
        out = os.path.join(self.d, "o.csv")
        add_hashes(self.src, out, ["id", "name"])
        rows = self.read(out)
        self.assertEqual(rows[0]["row_hash"], row_hash({"id": "1", "name": "Ann"}, ["id", "name"]))
        self.assertEqual(len(rows), 2)
    def test_no_concat_collision(self):
        self.assertNotEqual(row_hash({"a": "ab", "b": "c"}, ["a", "b"]), row_hash({"a": "a", "b": "bc"}, ["a", "b"]))
    def test_unknown_col(self):
        with self.assertRaises(ValueError):
            add_hashes(self.src, os.path.join(self.d, "x.csv"), ["nope"])

if __name__ == "__main__":
    unittest.main()
