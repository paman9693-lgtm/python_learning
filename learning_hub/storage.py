"""Small JSON-backed task and quiz-history store."""

import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any


class StorageError(RuntimeError):
    """Raised when learning-hub data cannot be read or written."""


def default_data_path() -> Path:
    """Return the user's data file location, allowing an environment override."""
    override = os.environ.get("PYTHON_LEARNING_HOME")
    data_directory = Path(override).expanduser() if override else Path.home() / ".python_learning_hub"
    return data_directory / "data.json"


class DataStore:
    """Persist practice tasks and quiz results in one JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_data_path()

    def load(self) -> dict[str, list[dict[str, Any]]]:
        try:
            with self.path.open(encoding="utf-8") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            return {"tasks": [], "quiz_results": []}
        except (json.JSONDecodeError, OSError) as error:
            raise StorageError(f"Could not read {self.path}: {error}") from error

        if not isinstance(data, dict):
            raise StorageError(f"Data in {self.path} must be a JSON object.")
        tasks = data.get("tasks", [])
        results = data.get("quiz_results", [])
        if not isinstance(tasks, list) or not isinstance(results, list):
            raise StorageError(f"Data in {self.path} has an invalid format.")
        return {"tasks": tasks, "quiz_results": results}

    def save(self, data: dict[str, list[dict[str, Any]]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                delete=False,
                suffix=".tmp",
            ) as data_file:
                temporary_path = Path(data_file.name)
                json.dump(data, data_file, indent=2, ensure_ascii=False)
                data_file.write("\n")
            temporary_path.replace(self.path)
        except OSError as error:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise StorageError(f"Could not save {self.path}: {error}") from error

    def add_task(self, title: str) -> dict[str, Any]:
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("A task title cannot be empty.")
        data = self.load()
        task = {"id": uuid.uuid4().hex[:8], "title": clean_title, "done": False}
        data["tasks"].append(task)
        self.save(data)
        return task

    def complete_task(self, task_id: str) -> dict[str, Any]:
        data = self.load()
        for task in data["tasks"]:
            if task.get("id") == task_id:
                task["done"] = True
                self.save(data)
                return task
        raise ValueError(f"No task found with id {task_id!r}.")

    def delete_task(self, task_id: str) -> None:
        data = self.load()
        remaining_tasks = [task for task in data["tasks"] if task.get("id") != task_id]
        if len(remaining_tasks) == len(data["tasks"]):
            raise ValueError(f"No task found with id {task_id!r}.")
        data["tasks"] = remaining_tasks
        self.save(data)

    def record_quiz_result(self, score: int, total: int) -> None:
        data = self.load()
        data["quiz_results"].append(
            {"score": score, "total": total, "percentage": round(score / total * 100)}
        )
        self.save(data)
