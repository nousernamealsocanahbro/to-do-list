import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.environ['DB_NAME'])
        self.cur = self.conn.cursor()
        self.lookup_table = {}

        self._update_lookup_table()

    def create_table(self) -> None:
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        priority INTEGER NULL DEFAULT 0,
        done INTEGER NULL DEFAULT 0,
        deadline TEXT NULL,
        date_finished TEXT NULL
        )
        """)

    def _get_tasks(self) -> list:
        self.cur.execute("""
        SELECT *
        FROM tasks
        ORDER BY priority DESC
        """)

        return self.cur.fetchall()

    def _validate_int(self, message: str) -> bool:
        try:
            int(message)

            return True
        except ValueError as e:
            print(e)
            
            return False

    def _get_id(self, message: str) -> int:
        while True:
            self.print_tasks()

            task_id = input(message)

            if self._validate_int(task_id):
                if int(task_id) in self.lookup_table:
                    return self.lookup_table[int(task_id)]
                else: 
                    print("ID not found in database, please try again.")

    def _write(self, command: str, values: tuple) -> None:
        self.cur.execute(command, values)
        self.conn.commit()
        self._update_lookup_table()

    def _get_task_details(self) -> tuple:
        task = input("Enter task: ")
        priority = input("Priority? (y/n): ").lower()
        has_deadline = input("Deadline? (y/n): ").lower()

        if has_deadline == 'y':
            deadline = input("Enter deadline (yyyy-mm-dd): ")
        else:
            deadline = None

        return task, (1 if priority == "y" else 0), deadline

    def _update_lookup_table(self):
        tasks = self._get_tasks()
        self.lookup_table.clear()

        for i, (task_id, _, _, _, _, _) in enumerate(tasks, start=1):
            self.lookup_table[i] = task_id

    def print_tasks(self) -> None:
        tasks = self._get_tasks()

        for i, (_, task, priority, done, deadline, date_finished) in enumerate(tasks, start=1):
            if done:
                print(f"{i}. {task} - Done on {date_finished}.")
            else:
                print(f"{i}. {"[PRIORITY] " if priority else ""}{task} - Not done. {"Deadline: " if deadline else ""}{deadline if deadline else ""}")

    def mark_task_as_done(self) -> None:
        task_id = self._get_id("Enter ID of task to mark as done: ")

        self._write("""
        UPDATE tasks
        SET done = TRUE,
        priority = desc,
        date_finished = DATE('now')
        WHERE id = ?
        """, 
        (task_id,))

    def add_task(self) -> None:
        task, priority, deadline = self._get_task_details()

        self._write("""
        INSERT INTO tasks (task, priority, deadline)
        VALUES (?, ?, ?)
        """,
        (task, priority, deadline))

    def modify_task(self) -> None:
        task_id = self._get_id("Enter number of task you wish to modify: ")

        task, priority, deadline = self._get_task_details()

        self._write("""
        UPDATE tasks
        SET task = ?,
        priority = ?,
        deadline = ?
        WHERE id = ?
        """,
        (task, priority, deadline, task_id))

    def remove_task(self) -> None:
        task_id = self._get_id("Enter number of task you wish to remove: ")

        self._write("""
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,))