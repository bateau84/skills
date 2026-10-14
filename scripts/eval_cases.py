"""Project-owned Loom-format normalization; no provider or runner imports."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(text: str):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f"non-finite JSON constant: {value}")

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def strings(value, where, *, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value) or not all(
        isinstance(s, str) and s.strip() for s in value
    ):
        raise ValueError(f"{where}: expected {'nonempty ' if nonempty else ''}string array")
    return tuple(value)


@dataclass(frozen=True)
class Case:
    id: str
    source_id: str | int
    skill: str
    prompt: str
    common_instruction: str
    expectations: tuple[str, ...]
    negative: tuple[str, ...]
    trap: str
    source: str
    source_sha256: str

    @property
    def selectors(self):
        # Bare numeric IDs are intentionally not global aliases.
        return (self.id, f"{self.skill}:{self.source_id}")

    def data(self):
        return {
            "skill": self.skill, "source_id": self.source_id, "prompt": self.prompt,
            "common_instruction": self.common_instruction,
            "expectations": list(self.expectations), "must_not": list(self.negative),
            "trap": self.trap,
        }


def normalize_document(doc, skill: str, source: str, sha256: str) -> tuple[Case, ...]:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill):
        raise ValueError(f"{source}: invalid skill directory name")
    if isinstance(doc, list):
        raw_cases, common = doc, ""
    elif isinstance(doc, dict):
        declared = doc.get("skill", doc.get("skill_name", skill))
        if declared != skill:
            raise ValueError(f"{source}: declared skill differs from folder {skill}")
        if "cases" in doc and "evals" in doc:
            raise ValueError(f"{source}: ambiguous cases/evals")
        raw_cases = doc.get("cases", doc.get("evals"))
        common = doc.get("common_instruction", "")
    else:
        raise ValueError(f"{source}: expected object or array")
    if not isinstance(common, str) or not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError(f"{source}: invalid instruction or empty cases/evals")
    cases = []
    for index, raw in enumerate(raw_cases):
        if not isinstance(raw, dict):
            raise ValueError(f"{source}: case must be object")
        sid = raw.get("id", index + 1)
        if not ((type(sid) is int and sid >= 1) or (
            isinstance(sid, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", sid)
        )):
            raise ValueError(f"{source}: invalid source ID {sid!r}")
        prompt = raw.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{source}: case {sid} has no prompt")
        trap = raw.get("trap", "")
        if trap is None:
            trap = ""
        if not isinstance(trap, str):
            raise ValueError(f"{source}: invalid trap")
        negative = raw.get("negative_expectations", raw.get("must_not", []))
        if negative is None:
            negative = []
        cases.append(Case(
            f"SKILL-{skill}-{sid}", sid, skill, prompt, common,
            strings(raw.get("expectations"), source, nonempty=True),
            strings(negative, source),
            trap.strip(), source, sha256,
        ))
    if len({c.id for c in cases}) != len(cases):
        raise ValueError(f"{source}: duplicate normalized IDs")
    return tuple(cases)


def discover(root: Path) -> tuple[Case, ...]:
    cases = []
    for path in sorted((root / "skills").glob("*/evals/*.json")):
        if path.is_symlink() or any(p.is_symlink() for p in (path.parent, path.parent.parent)):
            raise ValueError(f"symlink fixture is not allowed: {path}")
        skill = path.parent.parent.name
        if not (path.parent.parent / "SKILL.md").is_file():
            raise ValueError(f"fixture has no skill: {path}")
        data = path.read_bytes()
        cases.extend(normalize_document(strict_json(data.decode()), skill, path.relative_to(root).as_posix(), digest(data)))
    if not cases or len({c.id for c in cases}) != len(cases):
        raise ValueError("empty corpus or duplicate normalized IDs across files")
    return tuple(cases)


def markdown_document(text: str, skill: str) -> dict:
    """Lossless conversion of the reviewed PA/WD packet fields, not re-authoring."""
    common = re.search(r"^> (.+)$", text, re.M)
    if not common:
        raise ValueError("missing Markdown common instruction")
    sections = re.findall(
        r"^## (\w+) — ([^\n]+)\n\n\*\*Prompt:\*\* (.*?)\n\n"
        r"\*\*Evaluator observations:\*\* (.*?)(?=\n\n## |\Z)", text, re.M | re.S,
    )
    if not sections:
        raise ValueError("missing Markdown cases")
    return {
        "skill": skill, "version": "1.0.0", "shape": 1,
        "common_instruction": common.group(1),
        "cases": [{"id": sid, "name": name, "prompt": prompt,
                   "expectations": [observations.rstrip("\n")]} for sid, name, prompt, observations in sections],
    }
