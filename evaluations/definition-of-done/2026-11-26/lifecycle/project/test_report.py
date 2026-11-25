import csv
import io
import unittest

from report import export_csv


class ReportTests(unittest.TestCase):
    def test_header_and_empty(self):
        self.assertEqual(export_csv([]), "job_id,outcome\n")

    def test_roundtrip_special_characters(self):
        rows = [
            ("job,1", "succeeded,with warnings"),
            ('job"2', 'failed: "timeout"'),
            ("job\n3", "failed\nretry exhausted"),
            ('job,"\n4', 'failed,"\nterminal'),
            ("job\r\n5", "failed\r\ntimeout"),
            ("job\r6", "failed\rtimeout"),
        ]

        parsed = list(csv.reader(io.StringIO(export_csv(rows), newline="")))

        self.assertEqual(parsed, [["job_id", "outcome"]] + [list(r) for r in rows])

    def test_escaped_fields_and_lf_record_endings(self):
        rows = [("job,1", 'failed: "timeout"'), ("job\n2", "succeeded")]

        self.assertEqual(
            export_csv(rows),
            'job_id,outcome\n"job,1","failed: ""timeout"""\n'
            '"job\n2",succeeded\n',
        )

    def test_order_and_plain_values(self):
        self.assertEqual(
            export_csv([("b", "failed"), ("a", "succeeded")]),
            "job_id,outcome\nb,failed\na,succeeded\n",
        )

    def test_preserves_plain_value_conversion(self):
        self.assertEqual(export_csv([(42, None)]), "job_id,outcome\n42,None\n")


if __name__ == "__main__":
    unittest.main()
