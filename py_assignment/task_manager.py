from datetime import datetime, timedelta


class Task:
    """
    This represent an individual task with necessary attributes as defined.
    It actually encapsulates the core data of a task. It's makes easier for crud.
    """

    def __init__(
        self, title, description, completed=False, created_at=None, completed_at=None
    ):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at or datetime.now().isoformat()


class TaskManager:
    """
    This manager class actually reponsible for managing tasks including add, complete, list, report using storage's method.
    """

    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.completed = True
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        count_total_tasks = len(tasks)
        complete_tasks = [task for task in tasks if task.completed]
        count_completed_tasks = len(complete_tasks)
        completed_tasks_taken_time = timedelta()

        for task in complete_tasks:
            if isinstance(task.completed_at, str) and isinstance(task.created_at, str):
                try:
                    completed_at = datetime.fromisoformat(task.completed_at)
                    created_at = datetime.fromisoformat(task.created_at)
                    time_taken = completed_at - created_at
                    completed_tasks_taken_time += time_taken
                except ValueError:
                    continue

        if count_completed_tasks > 0:
            average_time = completed_tasks_taken_time / count_completed_tasks
        else:
            average_time = timedelta()

        average_seconds = average_time.total_seconds()
        average_hours, remainder = divmod(average_seconds, 3600)
        average_minutes, average_seconds = divmod(remainder, 60)

        report = {
            "total": count_total_tasks,
            "completed": count_completed_tasks,
            "pending": count_total_tasks - count_completed_tasks,
            "average completed time": f"{int(average_hours)}h {int(average_minutes)}m {int(average_seconds)}s",
        }

        return report
