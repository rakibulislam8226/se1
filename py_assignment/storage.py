import json
import redis

from task_manager import Task


class Storage:

    def __init__(self):
        """Initialization redis database as persistent storage"""
        self.database = redis.Redis(host="localhost", port=6379, db=0)

    def save_task(self, task):
        """Saving task data into database by reading from json and store in db as key=title"""
        task_data = json.dumps(task.__dict__)
        self.database.set(task.title, task_data)

    def update_task(self, updated_task):
        """Update task also use the save_task method"""
        self.save_task(updated_task)

    def get_task(self, title):
        """Get the task based on title for complete and others where needed a single task"""
        if task_title := self.database.get(title):
            task_dict = json.loads(task_title)
            return Task(**task_dict)
        return None

    def get_all_tasks(self):
        """For getting all the tasks from database"""
        try:
            task_keys = self.database.keys()
            # Bulk fetch all the task values corosponding to the keys
            task_values = self.database.mget(task_keys)
            # using dictionary unpacking (**)
            tasks = [
                Task(**json.loads(task_data)) for task_data in task_values if task_data
            ]
            return tasks
        except Exception as e:
            print(f"Unexpected error while retriving tasks: {e}")

    def clear_all_tasks(self):
        """To delete all the tasks"""
        self.database.flushdb()
