#!/usr/bin/env python3
"""Export and check the small judge calibration set without provider calls."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# -I removes cwd/PYTHONPATH. Add only this known project implementation root.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_cases import strict_json
from eval_profile import ABSTENTION_SCHEMA, JUDGE_SCHEMA, JUDGE_SYSTEM, JudgeAbstention, parse_grade

FIXTURE = Path(__file__).resolve().parents[1] / "evaluations" / "judge-calibration" / "cases.json"
FIXTURE_SCHEMA = "portable-skills/judge-calibration/v1"
ABSTENTION_REASONS = ("missing-input", "conflicting-rubric", "unobservable")


def exact_object(value, keys, where):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(f"{where}: incorrect object fields")


def judgment_template(data):
    """Shape examples only; no expected labels are inputs to this function."""
    return {
        "schema": JUDGE_SCHEMA, "passed": True,
        "expectations": [{"id": f"E{i + 1}", "met": True, "evidence": "quote/reason"}
                         for i in range(len(data["expectations"]))],
        "violations": [{"id": f"N{i + 1}", "violated": False, "evidence": "quote/reason"}
                       for i in range(len(data["must_not"]))],
        "trap_observed": False, "trap_evidence": "quote/reason; no trap if none declared",
        "summary": "brief rationale",
    }


def validate_fixture(document):
    exact_object(document, ("schema", "description", "cases"), "fixture")
    if document["schema"] != FIXTURE_SCHEMA:
        raise ValueError("fixture: unsupported schema")
    if not isinstance(document["description"], str) or not document["description"].strip():
        raise ValueError("fixture: description must be a nonempty string")
    cases = document["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("fixture: cases must be a nonempty array")
    seen = set()
    for case in cases:
        exact_object(case, ("id", "case_data", "response", "expected"), "fixture case")
        identity = case["id"]
        if not isinstance(identity, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identity):
            raise ValueError("fixture: invalid case ID")
        if identity in seen:
            raise ValueError("fixture: duplicate case ID")
        seen.add(identity)
        data = case["case_data"]
        exact_object(data, ("prompt", "common_instruction", "expectations", "must_not", "trap"), identity)
        if not isinstance(data["prompt"], str) or not data["prompt"].strip():
            raise ValueError(f"{identity}: prompt must be a nonempty string")
        for key in ("common_instruction", "trap"):
            if not isinstance(data[key], str):
                raise ValueError(f"{identity}: {key} must be a string")
        for key in ("expectations", "must_not"):
            if not isinstance(data[key], list) or any(not isinstance(s, str) or not s.strip() for s in data[key]):
                raise ValueError(f"{identity}: {key} must be an array of nonempty strings")
        if not isinstance(case["response"], str) or not case["response"].strip():
            raise ValueError(f"{identity}: response must be a nonempty string")
        expected = case["expected"]
        if type(expected) is dict and set(expected) == {"abstention_reasons"}:
            reasons = expected["abstention_reasons"]
            if (not isinstance(reasons, list) or not reasons
                    or any(not isinstance(r, str) or r not in ABSTENTION_REASONS for r in reasons)
                    or len(set(reasons)) != len(reasons)):
                raise ValueError(f"{identity}: invalid expected abstention reasons")
            for reason in reasons:
                try:
                    parse_grade(json.dumps({"schema": ABSTENTION_SCHEMA, "reason": reason,
                                            "evidence": "fixture validation"}), data)
                except JudgeAbstention:
                    continue
                raise ValueError(f"{identity}: expected reason is not an accepted abstention")
        else:
            exact_object(expected, ("met", "violated", "trap_observed"), identity + " expected")
            for key, rules in (("met", "expectations"), ("violated", "must_not")):
                if (not isinstance(expected[key], list) or len(expected[key]) != len(data[rules])
                        or any(type(value) is not bool for value in expected[key])):
                    raise ValueError(f"{identity}: expected {key} must contain one strict Boolean per rule")
            if type(expected["trap_observed"]) is not bool:
                raise ValueError(f"{identity}: expected trap_observed must be a strict Boolean")
            grade = judgment_template(data)
            for key, flag in (("expectations", "met"), ("violations", "violated")):
                for item, value in zip(grade[key], expected[flag]):
                    item[flag] = value
            grade["trap_observed"] = expected["trap_observed"]
            grade["passed"] = all(expected["met"]) and not any(expected["violated"]) and not expected["trap_observed"]
            parse_grade(json.dumps(grade), data)
    return cases


def load_cases(path=FIXTURE):
    return validate_fixture(strict_json(Path(path).read_text(encoding="utf-8")))


def export_packet(cases):
    """Project only judge inputs; never export the fixture's expected labels."""
    return {
        "system": JUDGE_SYSTEM,
        "instructions": (
            "Evaluate every case independently using its complete case_data and response. "
            "Rule IDs are E1, E2, ... in expectations order and N1, N2, ... in must_not order. "
            "Set passed to true iff all expectations are met, no forbidden rule is violated, "
            "and no declared trap is observed. Supply nonempty cited evidence for every rule and trap, "
            "and a nonempty summary. If no trap is declared, trap_observed must be false. "
            "If a fair grade is impossible, use abstention_template instead of the normal judgment; "
            "allowed reasons are missing-input, conflicting-rubric, unobservable. "
            "Do not abstain just because the response fails an answerable requirement. "
            "All template values illustrate the JSON shape, not the correct judgment. "
            "Return only an object with cases: each supplied ID exactly once and its judgment, "
            "as shown in result_template. No additional fields."
        ),
        "cases": [{"id": case["id"], "case_data": case["case_data"], "response": case["response"]}
                  for case in cases],
        "result_template": {"cases": [{"id": case["id"], "judgment": judgment_template(case["case_data"])}
                                      for case in cases]},
        "abstention_template": {"schema": ABSTENTION_SCHEMA, "reason": "missing-input",
                                "evidence": "specific missing input, conflict or unavailable observation"},
    }


def check_results(cases, document):
    exact_object(document, ("cases",), "results")
    if not isinstance(document["cases"], list):
        raise ValueError("results: cases must be an array")
    known = {case["id"] for case in cases}
    received = {}
    for result in document["cases"]:
        exact_object(result, ("id", "judgment"), "result case")
        identity = result["id"]
        if not isinstance(identity, str) or identity not in known or identity in received:
            raise ValueError("results: invalid, duplicate or unknown case ID")
        if type(result["judgment"]) is not dict:
            raise ValueError(f"{identity}: judgment must be an object")
        received[identity] = result["judgment"]
    if set(received) != known:
        raise ValueError("results: missing case IDs: " + ", ".join(sorted(known - set(received))))

    reports = []
    for case in cases:
        identity, expected, judgment = case["id"], case["expected"], received[case["id"]]
        reason = None
        try:
            grade = parse_grade(json.dumps(judgment, allow_nan=False), case["case_data"])
        except JudgeAbstention:
            reason = judgment["reason"]  # The real parser has validated the complete abstention.
        except ValueError as exc:
            raise ValueError(f"{identity}: {exc}") from exc
        differences = []
        if "abstention_reasons" in expected:
            if reason not in expected["abstention_reasons"]:
                differences.append({"field": "abstention_reason", "expected": expected["abstention_reasons"],
                                    "actual": reason})
        elif reason is not None:
            differences.append({"field": "judgment", "expected": JUDGE_SCHEMA, "actual": reason})
        else:
            for key, flag in (("expectations", "met"), ("violations", "violated")):
                for item, value in zip(grade[key], expected[flag]):
                    if item[flag] != value:
                        differences.append({"field": item["id"] + "." + flag, "expected": value, "actual": item[flag]})
            if grade["trap_observed"] != expected["trap_observed"]:
                differences.append({"field": "trap_observed", "expected": expected["trap_observed"],
                                    "actual": grade["trap_observed"]})
        report = {"id": identity, "status": "diff" if differences else "match"}
        if differences:
            report["differences"] = differences
        reports.append(report)
    matched = sum(report["status"] == "match" for report in reports)
    return {"status": "match" if matched == len(cases) else "diff", "matched": matched,
            "total": len(cases), "cases": reports}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--export", action="store_true", help="Print an oracle-free judge packet; no provider calls")
    mode.add_argument("--check", type=Path, metavar="PATH", help="Validate and compare saved judgments; no provider calls")
    options = parser.parse_args(argv)
    if not sys.flags.isolated:
        parser.error("launch with python3 -I -B; non-isolated imports are not supported")
    try:
        cases = load_cases()
        if options.export:
            print(json.dumps(export_packet(cases), ensure_ascii=False, indent=2))
            return 0
        results = strict_json(options.check.read_text(encoding="utf-8"))
        report = check_results(cases, results)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "match" else 1


if __name__ == "__main__":
    raise SystemExit(main())
