#!/usr/bin/env python3
"""Check observable behavior of the trusted manual fixture, not design quality."""
from __future__ import annotations

import argparse
import importlib
import sys
import unittest
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--stage", choices=("seed", "first", "second"), required=True)
    options = parser.parse_args()
    project = options.project.resolve(strict=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(project))
    modules = [importlib.import_module(f"jobqueue.{name}") for name in ("api", "cli", "scheduler", "model")]
    for module in modules:
        if not Path(module.__file__).resolve().is_relative_to(project):
            raise ValueError(f"{module.__name__} did not load from the selected project")
    entries, model = modules[:3], modules[3]
    eligible = ("failed",) if options.stage == "seed" else ("failed", "timed_out")

    class ContractTests(unittest.TestCase):
        def assert_rejected(self, entry, job, error, message):
            store = model.Store([] if job is None else [job])
            with self.assertRaises(error) as caught:
                entry.retry(store, "job")
            self.assertEqual(str(caught.exception), message)
            self.assertEqual(store.get("job"), job)
            self.assertEqual(store.writes, 0)

        def test_allowed_retries(self):
            for entry in entries:
                for state in eligible:
                    for attempts in (0, 2):
                        with self.subTest(entry=entry.__name__, state=state, attempts=attempts):
                            store = model.Store([model.Job("job", state, attempts, "keep")])
                            result = entry.retry(store, "job")
                            # Literal contract expectations; no production helper computes them.
                            self.assertEqual((result.id, result.state, result.attempts, result.last_error),
                                             ("job", "queued", attempts + 1, None))
                            self.assertEqual(store.get("job"), result)
                            self.assertEqual(store.writes, 1)
                            if options.stage == "second":
                                self.assertIs(result.retry_allowed, True)

        def test_missing_and_ineligible_jobs(self):
            states = ["queued", "running", "completed", "cancelled", "unknown"]
            if options.stage == "seed":
                states.append("timed_out")
            for entry in entries:
                with self.subTest(entry=entry.__name__, missing=True):
                    self.assert_rejected(entry, None, LookupError, "job not found")
                for state in states:
                    with self.subTest(entry=entry.__name__, state=state):
                        self.assert_rejected(entry, model.Job("job", state, 3, "keep"),
                                             ValueError, "job is not failed")

        def test_selects_requested_job_and_preserves_other_records(self):
            for entry in entries:
                for state in eligible:
                    with self.subTest(entry=entry.__name__, state=state):
                        unrelated = model.Job("job", "failed", 0, "keep other diagnostic")
                        selected = model.Job("requested", state, 1, "clear this diagnostic")
                        store = model.Store([unrelated, selected])
                        result = entry.retry(store, "requested")
                        self.assertEqual((result.id, result.state, result.attempts, result.last_error),
                                         ("requested", "queued", 2, None))
                        self.assertEqual(store.get("requested"), result)
                        self.assertEqual(store.get("job"), unrelated)
                        self.assertEqual(store.writes, 1)

        def test_limit_rejections(self):
            for entry in entries:
                for state in eligible:
                    for attempts in (3, 4):
                        with self.subTest(entry=entry.__name__, state=state, attempts=attempts):
                            self.assert_rejected(entry, model.Job("job", state, attempts, "keep"),
                                                 ValueError, "retry limit reached")

        def test_save_failure_preserves_state(self):
            for entry in entries:
                for state in eligible:
                    with self.subTest(entry=entry.__name__, state=state):
                        original = model.Job("job", state, 1, "keep")
                        store = model.Store([original])
                        store.fail_saves = True
                        with self.assertRaises(OSError) as caught:
                            entry.retry(store, "job")
                        self.assertEqual(str(caught.exception), "storage unavailable")
                        self.assertEqual(store.get("job"), original)
                        self.assertEqual(store.writes, 0)

        def test_permission_and_precedence(self):
            if options.stage != "second":
                return
            self.assertIs(model.Job("job", "failed").retry_allowed, True)
            for entry in entries:
                for state in eligible:
                    for attempts in (0, 3):
                        with self.subTest(entry=entry.__name__, state=state, attempts=attempts):
                            job = model.Job("job", state, attempts, "keep", retry_allowed=False)
                            self.assert_rejected(entry, job, PermissionError, "retry disabled")
                with self.subTest(entry=entry.__name__, state="running"):
                    job = model.Job("job", "running", 3, "keep", retry_allowed=False)
                    self.assert_rejected(entry, job, ValueError, "job is not failed")

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    if options.stage != "second":
        suite = unittest.TestSuite(test for test in suite if test._testMethodName != "test_permission_and_precedence")
    print(f"Selected project: {project}; contract stage: {options.stage}", flush=True)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
