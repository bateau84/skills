import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_cases import discover, normalize_document, markdown_document

ROOT = Path(__file__).resolve().parents[2]


class CaseTests(unittest.TestCase):
    def test_markdown_conversion_preserves_reviewed_cases_and_source_metadata(self):
        versions = {"product-acceptance": "1.0.0", "work-decomposition": "1.1.0"}
        for skill, count in (("product-acceptance", 9), ("work-decomposition", 9)):
            folder = ROOT / "skills" / skill / "evals"
            actual = json.loads((folder / "evals.json").read_text())
            expected = markdown_document((folder / "cases.md").read_text(), skill)
            self.assertEqual(actual["version"], versions[skill])
            self.assertEqual(actual["cases"], expected["cases"])
            self.assertEqual(actual["common_instruction"], expected["common_instruction"])
            self.assertEqual(len(actual["cases"]), count)

    def test_corpus_matches_fixture_inventory_and_preserves_source_ids(self):
        cases = discover(ROOT)
        expected = []
        for path in sorted((ROOT / "skills").glob("*/evals/*.json")):
            doc = json.loads(path.read_text())
            raw_cases = doc if isinstance(doc, list) else doc.get("cases", doc.get("evals"))
            self.assertIsInstance(raw_cases, list)
            source = path.relative_to(ROOT).as_posix()
            skill = path.parent.parent.name
            for index, raw in enumerate(raw_cases, start=1):
                expected.append((f"SKILL-{skill}-{raw.get('id', index)}", source))
        self.assertCountEqual([(c.id, c.source) for c in cases], expected)
        # Guard against an accidental loss of the reviewed corpus, but allow new cases.
        self.assertGreaterEqual(len(cases), 352)
        required = {f"SKILL-code-analysis-CodeAnalysis-{n:02d}" for n in range(1, 21)}
        self.assertTrue(required.issubset({c.id for c in cases}))
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
