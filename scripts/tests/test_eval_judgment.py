import copy
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_profile import JUDGE_SCHEMA, behavior_score, parse_grade, skill_value, score_counts


DATA = {"expectations": ["first", "second"], "must_not": ["forbidden"], "trap": "trap"}
GRADE = {"schema": JUDGE_SCHEMA, "passed": True,
         "expectations": [{"id": "E1", "met": True, "evidence": "first quote"},
                          {"id": "E2", "met": True, "evidence": "second quote"}],
         "violations": [{"id": "N1", "violated": False, "evidence": "no violation"}],
         "trap_observed": False, "trap_evidence": "no trap", "summary": "answer satisfies rubric"}


class JudgmentTests(unittest.TestCase):
    def test_strict_json_rule_ids_order_independent_exactly_once(self):
        grade = copy.deepcopy(GRADE)
        grade["expectations"].reverse()
        for text in (json.dumps(grade), "```json\n" + json.dumps(grade) + "\n```"):
            self.assertEqual(parse_grade(text, DATA), GRADE)
        for change in (
            lambda g: g["expectations"].pop(),
            lambda g: g["expectations"].append(g["expectations"][0]),
            lambda g: g["expectations"][1].update(id="E1"),
            lambda g: g["violations"][0].update(id="N2"),
            lambda g: g["expectations"][0].update(met=1),
            lambda g: g["violations"][0].update(violated="false"),
            lambda g: g["expectations"][0].update(evidence=""),
            lambda g: g.update(passed=False),
            lambda g: g.update(trap_observed=True),
        ):
            invalid = copy.deepcopy(GRADE)
            change(invalid)
            with self.assertRaises(ValueError):
                parse_grade(json.dumps(invalid), DATA)
        with self.assertRaises(ValueError):
            parse_grade(json.dumps(GRADE).replace('"passed": true', '"passed": true, "passed": false'), DATA)
        with self.assertRaises(ValueError):
            parse_grade("Here is your grade: " + json.dumps(GRADE), DATA)

    def test_boolean_scores_include_negative_rule_compliance_and_declared_trap(self):
        self.assertEqual(behavior_score(GRADE, True), 1)
        changed = copy.deepcopy(GRADE)
        changed["expectations"][0]["met"] = False
        changed["passed"] = False
        grade = parse_grade(json.dumps(changed), DATA)
        self.assertEqual(behavior_score(grade, True), .75)
        self.assertEqual(behavior_score(grade, False), 2 / 3)

    def test_10pp_policy_trap_fixed_regression_and_absolute_verdict_independent(self):
        for args, expected in (
            ((10, False, False), "material-improvement"), ((9.99, False, False), "improvement"),
            ((0, True, False), "material-improvement"), ((20, False, True), "regression"),
            ((-1, True, False), "regression"), ((0, False, False), "neutral"),
        ):
            self.assertEqual(skill_value(*args), expected)
        negative = copy.deepcopy(GRADE)
        negative["expectations"][0]["met"] = False
        negative["passed"] = False
        grade = parse_grade(json.dumps(negative), DATA)
        self.assertEqual(skill_value((behavior_score(grade, True) - .5) * 100, False, False), "material-improvement")
        self.assertFalse(grade["passed"])

    def test_rule_fractions_represent_exact_threshold_not_float_subtraction(self):
        from fractions import Fraction
        g = copy.deepcopy(GRADE)
        g["expectations"] = [{"id": f"E{i}", "met": i < 6, "evidence": "quote"} for i in range(10)]
        g["violations"] = []
        b = copy.deepcopy(g)
        b["expectations"][5]["met"] = False
        self.assertLess((behavior_score(g, False) - behavior_score(b, False)) * 100, 10)
        delta = float(100 * (Fraction(*score_counts(g, False)) - Fraction(*score_counts(b, False))))
        self.assertEqual(delta, 10)
        self.assertEqual(skill_value(delta, False, False), "material-improvement")


if __name__ == "__main__":
    unittest.main()
