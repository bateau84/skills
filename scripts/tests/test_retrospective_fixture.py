"""Static guard for the target-readable deep-retrospective evidence fixture.

The evaluator's grading rules belong in tool-backed-retrieval.md, not in this
file's source events. This check does NOT execute or score a model.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "skills/retrospective/evals/fixtures/contradictory-session.json"


class RetrospectiveEvidenceFixtureTests(unittest.TestCase):
    def test_target_visible_fixture_contains_source_records_not_grading_notes(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))
        # Neither a top-level "notes" instruction nor a "purpose" admonition
        # belongs in the target agent's evidence. Reject unexpected metadata.
        self.assertEqual(set(source), {"root_session_id", "sessions"})
        self.assertEqual(source["root_session_id"], "session_general")
        sessions = source["sessions"]
        self.assertEqual({s["id"] for s in sessions}, {"session_general", "session_coder"})
        for session in sessions:
            self.assertEqual(set(session), {"id", "parentID", "messages"})
            for message in session["messages"]:
                self.assertEqual(
                    set(message) - {"id", "type", "text", "tool", "status", "time"},
                    set(),
                    "Target-visible messages must carry only event facts, not grading rules",
                )
                self.assertIsInstance(message["id"], str)
                self.assertIsInstance(message["type"], str)
        by_id = {s["id"]: s for s in sessions}
        self.assertIsNone(by_id["session_general"]["parentID"])
        self.assertEqual(by_id["session_coder"]["parentID"], "session_general")

    def test_parent_and_child_still_contain_independently_checkable_events(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))
        events = [event for session in source["sessions"] for event in session["messages"]]
        by_id = {event["id"]: event for event in events}
        self.assertEqual(len(by_id), len(events), "Original event identifiers must be unique")
        self.assertEqual({f"msg_{i:03d}" for i in range(1, 9)}, set(by_id))
        self.assertEqual(by_id["msg_003"]["status"], "error")
        self.assertEqual(by_id["msg_004"]["status"], "completed")
        self.assertEqual(by_id["msg_007"]["status"], "pass")
        self.assertIn("privacy constraint", by_id["msg_005"]["text"])
        self.assertIn("not validated", by_id["msg_006"]["text"])
        self.assertEqual([by_id[f"msg_{i:03d}"]["time"] for i in range(1, 9)], list(range(1, 9)))


if __name__ == "__main__":
    unittest.main()
