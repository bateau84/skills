#!/usr/bin/env python3
"""Verify this retained response experiment; no provider or target calls."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from eval_calibration import packet_for_cases
from eval_profile import JudgeAbstention, parse_grade


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = read(HERE / "manifest.json")
    freeze = read(HERE / "freeze-manifest.json")
    for entry in freeze["files"]:
        assert sha(HERE / entry["name"]) == entry["sha256"], entry["name"]
    for path, expected in manifest["files"].items():
        assert sha(HERE / path) == expected, path
    tasks = {t["opaque_task_id"]: t for t in read(HERE / "tasks.json")["tasks"]}
    assert len(tasks) == freeze["task_count"]
    results = []
    for arm, provenance in manifest["arms"].items():
        runs = [r for r in manifest["runs"] if r["arm"] == arm]
        assert len(runs) == len(tasks) and {r["task"] for r in runs} == set(tasks)
        cases = []
        for run in runs:
            task = tasks[run["task"]]
            target_input = read(HERE / run["input"])
            response = read(HERE / run["output"])
            assert target_input["request"] == task["prompt"], run["id"]
            assert set(response) == {"response"} and isinstance(response["response"], str)
            assert response["response"].strip()
            cases.append({"id": run["id"], "response": response["response"], "case_data": {
                "prompt": task["prompt"], "common_instruction": "",
                "expectations": [c["text"] for c in task["criteria"]],
                "must_not": [], "trap": ""}})
        packet = read(HERE / provenance["judge_input"])
        # Full scenario, rubric, answer, system instruction and templates must
        # match; shortened or arm-specific judge prompts are not accepted.
        assert packet == packet_for_cases(cases), arm
        observed = read(HERE / provenance["judge_output"])
        assert set(observed) == {"cases"}
        assert len(observed["cases"]) == len(cases)
        by_id = {r["id"]: r for r in observed["cases"]}
        assert set(by_id) == {c["id"] for c in cases}
        for run, case in zip(runs, cases):
            record = by_id[case["id"]]
            assert set(record) == {"id", "judgment"}
            try:
                grade = parse_grade(json.dumps(record["judgment"]), case["case_data"])
            except JudgeAbstention:
                results.append({"arm": arm, "task": run["task"], "status": "non-evidence",
                                "reason": record["judgment"]["reason"]})
            else:
                results.append({"arm": arm, "task": run["task"], "passed": grade["passed"],
                                "criteria_met": sum(e["met"] for e in grade["expectations"]),
                                "criteria_total": len(grade["expectations"])})
    return {"status": "artifacts-verified", "tasks": len(tasks), "responses": len(results),
            "scope": "Byte identity and grade-schema verification only; criterion validity is recorded separately in comparison.json.",
            "prompts_and_rubrics_matched": True, "production_parser_used": True,
            "results": results}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
