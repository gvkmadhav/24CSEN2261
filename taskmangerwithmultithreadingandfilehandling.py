#Chatgpt
import threading
import time
import os
import logging
import unittest

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Custom exception for task manager
class TaskManagerError(Exception):
    pass

class Task:
    def __init__(self, task_name, duration):
        self.task_name = task_name
        self.duration = duration
        self.completed = False

    def run_task(self):
        """Simulate running the task by sleeping for the duration."""
        logging.info(f"Starting task: {self.task_name}")
        time.sleep(self.duration)
        self.completed = True
        logging.info(f"Task {self.task_name} completed.")

    def __str__(self):
        return f"Task({self.task_name}, Duration: {self.duration}s, Completed: {self.completed})"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()

    def add_task(self, task):
        """Add task to the manager."""
        if not isinstance(task, Task):
            raise TaskManagerError("Only Task instances can be added.")
        self.tasks.append(task)
        logging.info(f"Task '{task.task_name}' added to the task manager.")

    def start_all_tasks(self):
        """Start all tasks using multiple threads."""
        threads = []
        for task in self.tasks:
            thread = threading.Thread(target=task.run_task)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def save_task_data(self, filename='task_data.txt'):
        """Save the status of tasks to a file."""
        with open(filename, 'w') as f:
            for task in self.tasks:
                f.write(str(task) + "\n")
        logging.info(f"Task data saved to {filename}.")

    def load_task_data(self, filename='task_data.txt'):
        """Load task data from a file."""
        if not os.path.exists(filename):
            raise TaskManagerError(f"File '{filename}' not found.")
        
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                task_data = line.strip().split(',')
                task_name = task_data[0].split('(')[1].strip()
                duration = int(task_data[1].split(':')[1].strip().replace('s', ''))
                completed = task_data[2].split(':')[1].strip() == 'True'
                task = Task(task_name, duration)
                task.completed = completed
                self.add_task(task)
        logging.info(f"Task data loaded from {filename}.")

    def get_task_status(self):
        """Return the status of all tasks."""
        return [str(task) for task in self.tasks]

# Unit Test for TaskManager
class TestTaskManager(unittest.TestCase):
    def test_task_creation(self):
        task = Task("Test Task", 2)
        self.assertEqual(task.task_name, "Test Task")
        self.assertEqual(task.duration, 2)

    def test_add_task(self):
        manager = TaskManager()
        task = Task("New Task", 5)
        manager.add_task(task)
        self.assertIn(task, manager.tasks)

    def test_task_manager_file_handling(self):
        manager = TaskManager()
        task1 = Task("Task 1", 1)
        task2 = Task("Task 2", 2)
        manager.add_task(task1)
        manager.add_task(task2)
        manager.save_task_data('test_task_data.txt')
        manager.load_task_data('test_task_data.txt')
        self.assertEqual(len(manager.tasks), 2)

# Main function to demonstrate functionality
def main():
    manager = TaskManager()

    try:
        # Add tasks to the manager
        task1 = Task("Task 1", 3)
        task2 = Task("Task 2", 2)
        task3 = Task("Task 3", 4)

        manager.add_task(task1)
        manager.add_task(task2)
        manager.add_task(task3)

        # Start all tasks in parallel using multi-threading
        logging.info("Starting all tasks...")
        manager.start_all_tasks()

        # Save and load task data
        manager.save_task_data('task_data.txt')
        manager.load_task_data('task_data.txt')

        # Display task statuses
        for status in manager.get_task_status():
            print(status)

    except TaskManagerError as e:
        logging.error(f"Task Manager Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

    # Run unit tests
    logging.info("Running unit tests...")
    unittest.main(exit=False)

if __name__ == "__main__":
    main()
