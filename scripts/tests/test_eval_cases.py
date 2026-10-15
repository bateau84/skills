import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_cases import discover, normalize_document, markdown_document

ROOT = Path(__file__).resolve().parents[2]


class CaseTests(unittest.TestCase):
    def test_markdown_conversion_preserves_all_reviewed_fields_exactly(self):
        for skill, count in (("product-acceptance", 9), ("work-decomposition", 7)):
            folder = ROOT / "skills" / skill / "evals"
            actual = json.loads((folder / "evals.json").read_text())
            expected = markdown_document((folder / "cases.md").read_text(), skill)
            self.assertEqual(actual, expected)
            self.assertEqual(len(actual["cases"]), count)
        self.assertEqual(len(discover(ROOT)), 234)

    def test_existing_corpus_has_218_cases_without_changing_source_ids(self):
        cases = discover(ROOT)
        existing = [c for c in cases if c.skill not in {"product-acceptance", "work-decomposition"}]
        self.assertEqual(len(existing), 218)
        numeric = next(c for c in cases if c.id == "SKILL-python-testing-1")
        self.assertEqual(numeric.source_id, 1)
        self.assertEqual(numeric.selectors, (numeric.id, "python-testing:1"))

    def test_three_loom_formats(self):
        raw = {"prompt": "p", "expectations": ["e"], "must_not": ["n"]}
        for doc in ([raw], {"skill": "s", "cases": [raw]}, {"skill_name": "s", "evals": [raw]}):
            case = normalize_document(doc, "s", "skills/s/evals/x.json", "abc")[0]
            self.assertEqual(case.id, "SKILL-s-1")
            self.assertEqual(case.negative, ("n",))

    def test_mismatched_skill_empty_rules_bad_ids_and_duplicate_ids_rejected(self):
        valid = {"id": "X", "prompt": "p", "expectations": ["e"]}
        for doc in (
            {"skill": "other", "cases": [valid]},
            [{**valid, "expectations": []}],
            [{**valid, "id": True}],
            [valid, valid],
        ):
            with self.assertRaises(ValueError):
                normalize_document(doc, "s", "x", "abc")


if __name__ == "__main__":
    unittest.main()
