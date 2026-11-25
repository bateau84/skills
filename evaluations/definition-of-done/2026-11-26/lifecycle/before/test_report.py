import csv
import io
import unittest
from report import export_csv

class ReportTests(unittest.TestCase):
    def test_header_and_empty(self):
        self.assertEqual(export_csv([]), "job_id,outcome\n")
    def test_roundtrip_special_characters(self):
        rows = [("job,1", "succeeded"), ('job"2', "failed"), ("job\n3", "succeeded")]
        self.assertEqual(list(csv.reader(io.StringIO(export_csv(rows)))), [["job_id", "outcome"]] + [list(r) for r in rows])
    def test_order_and_plain_values(self):
        self.assertEqual(export_csv([("b", "failed"), ("a", "succeeded")]), "job_id,outcome\nb,failed\na,succeeded\n")

if __name__ == "__main__":
    unittest.main()
