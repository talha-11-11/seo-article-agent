from typing import Dict
from threading import Lock
from .schemas import Job, JobStatus


class JobStore:
    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}
        self._lock = Lock()

    def create(self, job: Job) -> Job:
        with self._lock:
            self._jobs[job.id] = job
        return job

    def update_status(self, job_id: str, status: JobStatus, error_message: str | None = None) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.status = status
            job.error_message = error_message

    def save_article(self, job_id: str, article) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.article = article

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)
