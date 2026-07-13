from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

import reader


class RegistryTests(unittest.TestCase):
    def test_all_registries_join_exactly(self):
        data = reader.get_combined_data()
        self.assertEqual(len(data), 1783)
        self.assertEqual(set(data["K3a1"]), {"hom", "kho", "vol"})

    def test_loader_rejects_duplicate_and_malformed_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text("[K3a1|first]\n[K3a1|second]\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                reader.load_database(path, True)
            path.write_text("not a record\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "malformed"):
                reader.load_database(path, True)

    def test_reproduces_committed_statistics(self):
        output = io.StringIO()
        with redirect_stdout(output):
            reader.main()
        expected = (reader.ROOT / "reader_log.txt").read_text(encoding="utf-8-sig")
        self.assertEqual(output.getvalue().splitlines(), expected.splitlines())

    def test_named_summary_values(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(reader.get_kho_stat()[0], 1549)
            self.assertEqual(reader.get_hom_stat()[0], 1669)
            self.assertEqual(reader.get_kho_hom_stat()[0], 1677)
            self.assertEqual(reader.get_vol_stat1(), (320400, 45))
            self.assertEqual(reader.get_prime_stat(), (781, 20))


if __name__ == "__main__":
    unittest.main()
