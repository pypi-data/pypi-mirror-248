import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

from seledri.worker import Worker


class Timekeeper:
    def __init__(
        self,
        persistence_file: Path,
        worker_instance: Worker,
        logfile: Path = None,
        logger: logging.Logger = None,
    ):
        """
        Initializes the Timekeeper class, responsible for managing and scheduling jobs.

        Args:
            persistence_file (Path): Path to the file used for persisting job data.
            worker_instance (Worker): An instance of the Worker class to execute scheduled tasks.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.persistence_file = persistence_file
        self.worker = worker_instance
        self.jobs = self.load_jobs()
        self.logfile = logfile or Path(os.getenv("LOGS"), "schedule.logs")
        self._configure_logging()
        self.reload_function_map()
        self.__reschedule_jobs__()

    def _configure_logging(self) -> None:
        """
        Configures logging for the Timekeeper class.
        """
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(self.logfile)
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def load_jobs(self) -> Dict[str, Any]:
        """
        Loads the jobs from the persistence file.

        Returns:
            Dict[str, Any]: A dictionary of jobs indexed by their IDs.
        """
        try:
            with open(self.persistence_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_jobs(self) -> None:
        """
        Saves the current jobs to the persistence file.
        """
        with open(self.persistence_file, "w") as file:
            json.dump(self.jobs, file, indent=4)

    def compute_hash(
        self, task_name: str, schedule_time: datetime, *args, **kwargs
    ) -> str:
        """
        Computes a hash for the given task and arguments.

        Args:
            task_name (str): The name of the task.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.

        Returns:
            str: A hash string representing the task and arguments.
        """
        args = args or ""
        kwargs = kwargs or ""
        return hashlib.sha256(
            str(f"{task_name}{schedule_time.isoformat()}{args}{kwargs}").encode()
        ).hexdigest()

    def add_job(self, task_name: str, schedule_time: datetime, **kwargs) -> str:
        """
        Adds a new job to the schedule.

        Args:
            task_name (str): The name of the task to schedule.
            schedule_time (datetime): The time at which the task should be executed.
            **kwargs: Keyword arguments to pass to the task.

        Returns:
            str: The ID of the scheduled job.
        """
        job_id = self.compute_hash(task_name, schedule_time, kwargs)
        self.jobs[job_id] = {
            "task": task_name,
            "created": datetime.now().isoformat(),
            "schedule_time": schedule_time.isoformat(),
            **kwargs,
        }
        self.save_jobs()
        self.logger.info(
            f"Received job {job_id} with task {task_name} to run at {schedule_time}"
        )
        self.schedule_job_to_worker(job_id)
        return job_id

    def schedule_job_to_worker(self, job_id: str) -> None:
        """
        Schedules a job to be executed by the worker.

        Args:
            job_id (str): The ID of the job to schedule.
        """
        job_info = self.jobs[job_id]
        schedule_time = datetime.fromisoformat(job_info["schedule_time"])
        self.worker.__schedule_task__(
            job_info["task"],
            schedule_time,
            job_id,
            self.remove_job,
            **job_info["kwargs"],
        )

    def reload_function_map(self) -> None:
        """
        Reloads the function map from the Worker instance.
        """
        for func_identifier, func_data in self.worker.function_map.function_map.items():
            func = self.worker.function_map.deserialize_func(func_data)
            self.worker.register_task(func, func_identifier)
        self.logger.debug("Function map reloaded.")

    def __reschedule_jobs__(self) -> None:
        """
        Reschedules all jobs that are due to run.
        """
        self.logger.debug(f"Found {len(self.jobs)} scheduled.")
        now = datetime.now()
        self.prune()
        for job_id, job_info in self.jobs.items():
            schedule_time = datetime.fromisoformat(job_info["schedule_time"])
            if schedule_time < now:
                schedule_time = now + timedelta(seconds=10)
                self.logger.info(f"Rescheduling job {job_id} to run at {schedule_time}")
            self.worker.__schedule_task__(
                job_info["task"],
                schedule_time,
                job_id,
                self.remove_job,
                **job_info["kwargs"],
            )

    def remove_job(self, job_id: str) -> None:
        """
        Removes a job from the schedule.

        Args:
            job_id (str): The unique identifier of the job to remove.
        """
        self.jobs.pop(job_id)
        self.save_jobs()
        self.logger.info(f"Job {job_id} removed.")

    def prune(self) -> None:
        """
        Removes jobs that are no longer valid or have passed their schedule time.
        """
        now = datetime.now()
        jobs_to_remove = [
            job_id
            for job_id, job_info in self.jobs.items()
            if datetime.fromisoformat(job_info["schedule_time"]) < now
        ]
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
            self.logger.info(f"Pruned job {job_id}")
        self.save_jobs()

    def get_jobs(self) -> Dict[str, Any]:
        """
        Returns the currently scheduled jobs.

        Returns:
            Dict[str, Any]: A dictionary of the scheduled jobs.
        """
        return self.jobs
