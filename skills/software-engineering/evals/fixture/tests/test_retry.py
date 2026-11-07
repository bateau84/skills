import unittest

from jobqueue import api, cli, scheduler
from jobqueue.model import Job, Store


class RetryTests(unittest.TestCase):
    def test_failed_job_is_queued_and_diagnostic_is_cleared(self):
        for entry in (api, cli, scheduler):
            with self.subTest(entry=entry.__name__):
                store = Store([Job("job", "failed", 1, "timeout")])
                result = entry.retry(store, "job")
                self.assertEqual(result, Job("job", "queued", 2, None))
                self.assertEqual(store.get("job"), result)
                self.assertEqual(store.writes, 1)

    def test_rejections_do_not_write(self):
        for entry in (api, cli, scheduler):
            for job, error, message in (
                (None, LookupError, "job not found"),
                (Job("job", "running", 3, "keep"), ValueError, "job is not failed"),
                (Job("job", "failed", 3, "keep"), ValueError, "retry limit reached"),
            ):
                with self.subTest(entry=entry.__name__, job=job):
                    store = Store([] if job is None else [job])
                    with self.assertRaises(error) as caught:
                        entry.retry(store, "job")
                    self.assertEqual(str(caught.exception), message)
                    self.assertEqual(store.get("job"), job)
                    self.assertEqual(store.writes, 0)

    def test_failed_save_preserves_the_record(self):
        for entry in (api, cli, scheduler):
            with self.subTest(entry=entry.__name__):
                original = Job("job", "failed", 1, "keep")
                store = Store([original])
                store.fail_saves = True
                with self.assertRaisesRegex(OSError, "^storage unavailable$"):
                    entry.retry(store, "job")
                self.assertEqual(store.get("job"), original)
                self.assertEqual(store.writes, 0)


if __name__ == "__main__":
    unittest.main()
