from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Job:
    id: str
    state: str
    attempts: int = 0
    last_error: str | None = None


class Store:
    def __init__(self, jobs: list[Job]):
        self._jobs = {job.id: replace(job) for job in jobs}
        self.fail_saves = False
        self.writes = 0

    def get(self, job_id: str) -> Job | None:
        job = self._jobs.get(job_id)
        return replace(job) if job is not None else None

    def save(self, job: Job) -> None:
        if self.fail_saves:
            raise OSError("storage unavailable")
        self._jobs[job.id] = replace(job)
        self.writes += 1
