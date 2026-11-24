import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_calibration import FIXTURE, check_results, export_packet, load_cases, validate_fixture
from eval_profile import ABSTENTION_SCHEMA, JUDGE_SCHEMA, JUDGE_SYSTEM, JudgeAbstention, parse_grade

SCRIPT = Path(__file__).resolve().parents[1] / "eval_calibration.py"


def observations(cases):
    results = []
    for case in cases:
        expected = case["expected"]
        if "abstention_reasons" in expected:
            grade = {"schema": ABSTENTION_SCHEMA, "reason": expected["abstention_reasons"][0],
                     "evidence": "The task setup supplies no repository or execution capability."}
        else:
            grade = {
                "schema": JUDGE_SCHEMA,
                "passed": all(expected["met"]) and not any(expected["violated"]) and not expected["trap_observed"],
                "expectations": [{"id": f"E{i + 1}", "met": value, "evidence": "Fixture test evidence."}
                                 for i, value in enumerate(expected["met"])],
                "violations": [{"id": f"N{i + 1}", "violated": value, "evidence": "Fixture test evidence."}
                               for i, value in enumerate(expected["violated"])],
                "trap_observed": expected["trap_observed"], "trap_evidence": "Fixture test evidence.",
                "summary": "Synthetic parser input, not a model observation.",
            }
        results.append({"id": case["id"], "judgment": grade})
    return {"cases": results}


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases()
        self.results = observations(self.cases)

    def test_six_reviewed_cases_and_expected_labels_are_valid(self):
        self.assertEqual({case["id"] for case in self.cases}, {
            "equivalent-iterable", "conditional-regeneration", "invented-interface",
            "absent-execution-fixture", "presentation-is-not-action-order", "polished-wrong-answer-and-injection",
        })
        self.assertEqual(check_results(self.cases, self.results)["matched"], 6)
        for mutate in (
            lambda d: d.update(schema="unknown"),
            lambda d: d["cases"].append(copy.deepcopy(d["cases"][0])),
            lambda d: d["cases"][0]["expected"].update(met=[1]),
            lambda d: d["cases"][0]["expected"].update(met=[]),
            lambda d: d["cases"][0]["expected"].update(trap_observed=0),
            lambda d: d["cases"][0]["expected"].update(extra=True),
            lambda d: d["cases"][3].update(expected={"met": [True], "violated": [], "trap_observed": True}),
            lambda d: d["cases"][3]["expected"].update(abstention_reasons=["unknown"]),
            lambda d: d["cases"][3]["expected"].update(abstention_reasons=["missing-input", "missing-input"]),
        ):
            document = json.loads(FIXTURE.read_text(encoding="utf-8"))
            mutate(document)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                validate_fixture(document)

    def test_export_withholds_oracle_and_preserves_all_judge_inputs(self):
        packet = export_packet(self.cases)
        self.assertEqual(packet["system"], JUDGE_SYSTEM)
        self.assertNotIn('"expected"', json.dumps(packet))
        changed = copy.deepcopy(self.cases)
        changed[0]["expected"]["met"] = [False]
        changed[3]["expected"]["abstention_reasons"] = ["unobservable"]
        self.assertEqual(export_packet(changed), packet)
        for source, exported, template in zip(self.cases, packet["cases"], packet["result_template"]["cases"]):
            self.assertEqual(exported, {key: source[key] for key in ("id", "case_data", "response")})
            self.assertEqual(template["id"], source["id"])
            parse_grade(json.dumps(template["judgment"]), source["case_data"])
        with self.assertRaises(JudgeAbstention):
            parse_grade(json.dumps(packet["abstention_template"]), self.cases[0]["case_data"])

    def test_result_envelope_rejects_missing_duplicate_invalid_and_extra_ids(self):
        for mutate in (
            lambda d: d["cases"].pop(),
            lambda d: d["cases"].append(copy.deepcopy(d["cases"][0])),
            lambda d: d["cases"][0].update(id="unknown"),
            lambda d: d["cases"][0].update(id=1),
            lambda d: d["cases"][0].update(id=[]),
            lambda d: d["cases"][0].update(extra=True),
            lambda d: d["cases"][0].update(judgment="{}"),
            lambda d: d.update(cases={}),
            lambda d: d.update(extra=True),
        ):
            document = copy.deepcopy(self.results)
            mutate(document)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                check_results(self.cases, document)

    def test_checker_uses_real_strict_grade_validation(self):
        for mutate in (
            lambda g: g.update(passed=False),
            lambda g: g["expectations"][0].update(met=1),
            lambda g: g["expectations"][0].update(evidence=""),
            lambda g: g["expectations"][0].update(id="E2"),
            lambda g: g["expectations"].append(copy.deepcopy(g["expectations"][0])),
            lambda g: g.update(extra=True),
        ):
            document = copy.deepcopy(self.results)
            mutate(document["cases"][0]["judgment"])
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                check_results(self.cases, document)

    def test_every_boolean_is_compared_even_when_overall_failure_is_unchanged(self):
        grade = self.results["cases"][-1]["judgment"]
        grade["expectations"][0]["met"] = True
        grade["expectations"][1]["met"] = False
        grade["violations"][0]["violated"] = False
        grade["trap_observed"] = False
        self.assertFalse(grade["passed"])
        report = check_results(self.cases, self.results)
        self.assertEqual((report["status"], report["matched"], report["total"]), ("diff", 5, 6))
        self.assertEqual(report["cases"][-1]["differences"], [
            {"field": "E1.met", "expected": False, "actual": True},
            {"field": "E2.met", "expected": True, "actual": False},
            {"field": "N1.violated", "expected": True, "actual": False},
            {"field": "trap_observed", "expected": True, "actual": False},
        ])

    def test_equivalent_abstention_labels_are_accepted_and_other_labels_differ(self):
        for reason in ("missing-input", "unobservable", "conflicting-rubric"):
            self.results["cases"][3]["judgment"]["reason"] = reason
            report = check_results(self.cases, self.results)
            self.assertEqual(report["status"], "diff" if reason == "conflicting-rubric" else "match")
        self.results["cases"][0]["judgment"] = copy.deepcopy(self.results["cases"][3]["judgment"])
        self.assertEqual(check_results(self.cases, self.results)["cases"][0]["status"], "diff")
        self.results["cases"][3]["judgment"] = observations(self.cases)["cases"][0]["judgment"]
        self.assertEqual(check_results(self.cases, self.results)["cases"][3]["status"], "diff")

    def test_result_and_rule_order_do_not_change_comparison(self):
        before = copy.deepcopy(self.results)
        self.results["cases"].reverse()
        for result in self.results["cases"]:
            result["judgment"].get("expectations", []).reverse()
        self.assertEqual(check_results(self.cases, self.results), check_results(self.cases, before))

    def test_real_cli_isolated_export_and_check_exit_statuses(self):
        with tempfile.TemporaryDirectory() as temp:
            base = [sys.executable, "-I", "-B", str(SCRIPT)]
            exported = subprocess.run([*base, "--export"], cwd=temp, capture_output=True, text=True, timeout=10)
            self.assertEqual(exported.returncode, 0, exported.stderr)
            self.assertEqual(json.loads(exported.stdout), export_packet(self.cases))
            path = Path(temp) / "observations.json"
            for expected_code in (0, 1, 2):
                if expected_code == 1:
                    self.results["cases"][3]["judgment"]["reason"] = "conflicting-rubric"
                elif expected_code == 2:
                    self.results["cases"].pop()
                path.write_text(json.dumps(self.results), encoding="utf-8")
                checked = subprocess.run([*base, "--check", str(path)], cwd=temp,
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(checked.returncode, expected_code, checked.stderr)
                if expected_code != 2:
                    self.assertEqual(json.loads(checked.stdout)["status"], "match" if expected_code == 0 else "diff")
                else:
                    self.assertEqual(checked.stdout, "")
            unisolated = subprocess.run([sys.executable, "-B", str(SCRIPT), "--export"], cwd=temp,
                                       capture_output=True, text=True, timeout=10)
            self.assertEqual(unisolated.returncode, 2)
            self.assertIn("python3 -I -B", unisolated.stderr)

    def test_cli_rejects_duplicate_json_keys_and_nonfinite_numbers(self):
        valid = json.dumps(self.results)
        for text in ('{"cases": [], "cases": []}',
                     valid.replace('"passed": true', '"passed": true, "passed": false', 1),
                     valid.replace('"passed": true', '"passed": NaN', 1)):
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "invalid.json"
                path.write_text(text, encoding="utf-8")
                result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--check", str(path)],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
