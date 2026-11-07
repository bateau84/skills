from dataclasses import replace

from .model import Job, Store


def retry(store: Store, job_id: str) -> Job:
    job = store.get(job_id)
    if job is None:
        raise LookupError("job not found")
    if job.state != "failed":
        raise ValueError("job is not failed")
    if job.attempts >= 3:
        raise ValueError("retry limit reached")
    updated = replace(job, state="queued", attempts=job.attempts + 1, last_error=None)
    store.save(updated)
    return updated
