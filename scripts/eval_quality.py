"""Deterministic outcome/convention projections, separate from model judgments.

Missing labels are unknown, not outcomes. Authored case purpose never proves
that a case discriminates; calibration needs separate observed run evidence.
"""
from __future__ import annotations

from fractions import Fraction


def score_axes(grade, data):
    types = data.get("evaluation", {}).get("criterion_types", {})
    counts = {kind: [0, 0] for kind in ("outcome", "convention", "unclassified")}
    rules = [(item["id"], item["met"]) for item in grade["expectations"]]
    rules += [(item["id"], not item["violated"]) for item in grade["violations"]]
    if data["trap"]:
        rules.append(("T1", not grade["trap_observed"]))
    for identity, satisfied in rules:
        count = counts[types.get(identity, "unclassified")]
        count[0] += satisfied
        count[1] += 1
    return {kind: {"satisfied": n, "total": total, "score": n / total if total else None,
                   "passed": n == total if total else None}
            for kind, (n, total) in counts.items()}


def axis_delta(baseline, candidate, kind):
    b, c = baseline[kind], candidate[kind]
    if not b["total"] or not c["total"]:
        return None
    return float(100 * (Fraction(c["satisfied"], c["total"]) - Fraction(b["satisfied"], b["total"])))


def axis_text(axis):
    """Closed presentation vocabulary: never echo arbitrary callback fields."""
    if not isinstance(axis, dict):
        return "unavailable"
    n, total = axis.get("satisfied"), axis.get("total")
    if type(n) is not int or type(total) is not int or not 0 <= n <= total or total == 0:
        return "unavailable"
    return f"{n}/{total} ({'PASS' if n == total else 'FAIL'})"


def public_axes(axes):
    """Project only validated counts; do not publish arbitrary callback values."""
    if not isinstance(axes, dict):
        return {}
    result = {}
    for kind in ("outcome", "convention", "unclassified"):
        axis = axes.get(kind)
        if not isinstance(axis, dict):
            continue
        n, total = axis.get("satisfied"), axis.get("total")
        if type(n) is int and type(total) is int and 0 <= n <= total:
            result[kind] = {"satisfied": n, "total": total, "score": n / total if total else None,
                            "passed": n == total if total else None}
    return result


def judge_relationship(target, judge):
    """Conservative selector check, not verified underlying model identity.

    Provider aliases and deployment names can still hide an identical model.
    A different provider or reasoning variant is not by itself a different model.
    """
    def model_name(value):
        return value.split("#", 1)[0].rsplit("/", 1)[-1].lower()
    return "same-model-selector" if model_name(target) == model_name(judge) else "different-selectors-unverified"
