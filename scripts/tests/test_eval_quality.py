import copy
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_cases import normalize_document
from eval_profile import ABSTENTION_SCHEMA, JudgeAbstention, SkillsComparison, parse_grade
from eval_quality import axis_delta, judge_relationship, score_axes
from test_eval_judgment import DATA, GRADE


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.data = {**DATA, "evaluation": {"mode": "response", "purpose": "contrast",
                     "criterion_types": {"E1": "outcome", "E2": "convention", "N1": "outcome", "T1": "outcome"}}}

    def test_legacy_criteria_remain_unclassified_not_outcomes(self):
        axes = score_axes(GRADE, DATA)
        self.assertEqual(axes["unclassified"]["total"], 4)
        self.assertIsNone(axes["outcome"]["passed"])
        self.assertIsNone(axis_delta(axes, axes, "outcome"))

    def test_conventions_cannot_compensate_for_a_worse_outcome(self):
        before, after = copy.deepcopy(GRADE), copy.deepcopy(GRADE)
        before["expectations"][1]["met"] = False
        after["expectations"][0]["met"] = False
        before["passed"] = after["passed"] = False
        def outcome(grade):
            return SimpleNamespace(semantic=SimpleNamespace(data={"grade": grade, "score": .75}),
                classification="fail", case=SimpleNamespace(project_data=self.data),
                deterministic_checks=[SimpleNamespace(name="treatment-integrity", status="pass")])
        api = SimpleNamespace(ComparisonDecision=lambda classification, summary, data:
                              SimpleNamespace(classification=classification, summary=summary, data=data))
        decision = SkillsComparison(SimpleNamespace(eval_api=api)).compare_pair(outcome(before), outcome(after))
        self.assertEqual(decision.classification, "regression")
        self.assertEqual(decision.data["rubric_delta_pp"], 0)
        self.assertLess(decision.data["outcome_delta_pp"], 0)
        self.assertGreater(decision.data["convention_delta_pp"], 0)

    def test_convention_trap_does_not_change_outcome_comparison(self):
        self.data["evaluation"]["criterion_types"]["T1"] = "convention"
        after = copy.deepcopy(GRADE)
        after["trap_observed"] = True
        after["passed"] = False
        axes = score_axes(after, self.data)
        self.assertTrue(axes["outcome"]["passed"])
        self.assertFalse(axes["convention"]["passed"])
        def compare(data):
            def outcome(grade):
                return SimpleNamespace(semantic=SimpleNamespace(data={"grade": grade, "score": 1 if grade["passed"] else .75}),
                    classification="pass" if grade["passed"] else "fail", case=SimpleNamespace(project_data=data),
                    deterministic_checks=[SimpleNamespace(name="treatment-integrity", status="pass")])
            api = SimpleNamespace(ComparisonDecision=lambda classification, summary, data:
                                  SimpleNamespace(classification=classification, summary=summary, data=data))
            return SkillsComparison(SimpleNamespace(eval_api=api)).compare_pair(outcome(GRADE), outcome(after))
        self.assertEqual(compare(self.data).classification, "neutral")
        self.data["evaluation"]["criterion_types"]["T1"] = "outcome"
        self.assertEqual(compare(self.data).classification, "regression")
        self.data["evaluation"]["criterion_types"] = dict.fromkeys(("E1", "E2", "N1", "T1"), "convention")
        convention_only = compare(self.data)
        self.assertEqual(convention_only.classification, "regression")
        self.assertEqual(convention_only.data["score_basis"], "convention")
        self.assertIsNone(convention_only.data["outcome_delta_pp"])

    def test_contract_is_complete_and_cannot_claim_execution_or_calibration(self):
        raw = {"id": "X", "prompt": "Supplied task", "expectations": DATA["expectations"],
               "must_not": DATA["must_not"], "trap": DATA["trap"], "evaluation": self.data["evaluation"]}
        case = normalize_document([raw], "s", "s/evals.json", "hash")[0]
        self.assertEqual(case.data()["evaluation"], self.data["evaluation"])
        for change in (
            lambda e: e.update(mode="execution"),
            lambda e: e.update(purpose="discriminating"),
            lambda e: e.update(purpose=[]),
            lambda e: e.update(calibration="proven"),
            lambda e: e["criterion_types"].pop("N1"),
            lambda e: e["criterion_types"].update(E9="outcome"),
            lambda e: e["criterion_types"].update(E1="unclassified"),
        ):
            invalid = copy.deepcopy(raw)
            change(invalid["evaluation"])
            with self.assertRaises(ValueError):
                normalize_document([invalid], "s", "s/evals.json", "hash")

    def test_abstention_never_turns_missing_inputs_into_failed_work(self):
        for reason in ("missing-input", "conflicting-rubric", "unobservable"):
            with self.assertRaises(JudgeAbstention):
                parse_grade(json.dumps({"schema": ABSTENTION_SCHEMA, "reason": reason,
                                        "evidence": "The requested diff is absent."}), DATA)
        for reason in ("answer-is-wrong", [], None):
            with self.assertRaises(ValueError):
                parse_grade(json.dumps({"schema": ABSTENTION_SCHEMA, "reason": reason, "evidence": "x"}), DATA)

    def test_different_provider_or_reasoning_does_not_establish_independent_model(self):
        for target, judge in (("openai/m", "proxy/m"), ("openai/m#high", "openai/m#low"),
                              ("proxy/vendor/m", "vendor/m"), ("test/model", "test/model#reasoning/high")):
            self.assertEqual(judge_relationship(target, judge), "same-model-selector")
        self.assertEqual(judge_relationship("vendor/a", "vendor/b"), "different-selectors-unverified")


if __name__ == "__main__":
    unittest.main()
