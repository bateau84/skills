"""Source-only deep-retrospective fixture guards; no model is executed.

The evaluator rubric lives in tool-backed-retrieval.md, not in the fixture.
The checks below protect both the chronology and evidence provenance: a
worker's failed edit is not equivalent to a parent's unrelated failed tool.
"""
from __future__ import annotations

from copy import deepcopy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "skills/retrospective/evals/fixtures/contradictory-session.json"
PARENT_IDS = ("msg_001", "msg_002", "msg_005", "msg_008")
CHILD_IDS = ("msg_003", "msg_004", "msg_006", "msg_007")


class RetrospectiveEvidenceFixtureTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assert_source_evidence(self, source):
        """Reusable oracle so in-memory mutations exercise the same assertions."""
        self.assertEqual(source["root_session_id"], "session_general")
        sessions = {s["id"]: s for s in source["sessions"]}
        self.assertEqual(len(sessions), 2)
        self.assertEqual(set(sessions), {"session_general", "session_coder"})
        self.assertIsNone(sessions["session_general"]["parentID"])
        self.assertEqual(sessions["session_coder"]["parentID"], "session_general")

        parent = {m["id"]: m for m in sessions["session_general"]["messages"]}
        child = {m["id"]: m for m in sessions["session_coder"]["messages"]}
        self.assertEqual(len(parent), len(sessions["session_general"]["messages"]), "Duplicate parent message IDs")
        self.assertEqual(len(child), len(sessions["session_coder"]["messages"]), "Duplicate child message IDs")
        self.assertEqual(tuple(parent), PARENT_IDS, "session_general must retain user/delegation/correction/final events")
        self.assertEqual(tuple(child), CHILD_IDS, "session_coder must retain its four worker events")

        expected = {
            "msg_001": {"type": "user"},
            "msg_002": {"type": "assistant"},
            "msg_003": {"type": "tool", "tool": "edit", "status": "error"},
            "msg_004": {"type": "tool", "tool": "edit", "status": "completed"},
            "msg_005": {"type": "user"},
            "msg_006": {"type": "review"},
            "msg_007": {"type": "test", "status": "pass"},
            "msg_008": {"type": "assistant"},
        }
        by_id = {**parent, **child}
        for message_id, fields in expected.items():
            actual = {field: by_id[message_id].get(field) for field in fields}
            self.assertEqual(actual, fields, f"{message_id} must preserve its original source event")
        self.assertIn("privacy rules", parent["msg_001"]["text"])
        self.assertIn("privacy constraint", parent["msg_005"]["text"])
        self.assertIn("not validated", child["msg_006"]["text"])
        self.assertIn("final tests passed", parent["msg_008"]["text"])
        for message_id, message in by_id.items():
            self.assertEqual(message["time"], int(message_id[-3:]), f"{message_id} chronology changed")

    def test_target_visible_fixture_contains_source_records_not_grading_notes(self):
        source = self.load_fixture()
        self.assertEqual(set(source), {"root_session_id", "sessions"})
        for session in source["sessions"]:
            self.assertEqual(set(session), {"id", "parentID", "messages"})
            for message in session["messages"]:
                self.assertEqual(set(message) - {"id", "type", "text", "tool", "status", "time"}, set())
                self.assertIsInstance(message["id"], str)
                self.assertIsInstance(message["type"], str)

    def test_parent_and_child_events_preserve_ownership_type_and_outcome(self):
        self.assert_source_evidence(self.load_fixture())

    def test_transplanting_child_events_to_parent_is_detected(self):
        mutant = deepcopy(self.load_fixture())
        sessions = {s["id"]: s for s in mutant["sessions"]}
        sessions["session_general"]["messages"].extend(sessions["session_coder"]["messages"])
        sessions["session_coder"]["messages"] = []
        with self.assertRaisesRegex(AssertionError, "session_general must retain"):
            self.assert_source_evidence(mutant)

    def test_relabelled_failed_edit_as_read_is_detected(self):
        mutant = deepcopy(self.load_fixture())
        child = next(s for s in mutant["sessions"] if s["id"] == "session_coder")
        failed = next(m for m in child["messages"] if m["id"] == "msg_003")
        failed["tool"] = "read"
        with self.assertRaisesRegex(AssertionError, "msg_003 must preserve"):
            self.assert_source_evidence(mutant)


if __name__ == "__main__":
    unittest.main()
