import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self) -> None:
        self.connection = self._connect_to_db()
        self.cursor = self.connection.cursor()
        self.lookup_table = self._return_lookup_table()

    def _connect_to_db(self):
        return mysql.connector.connect(
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASSWORD'],
            database = os.environ['DB_NAME'],
            host = os.environ['DB_HOST'],
        )

    def _get_tasks(self) -> list:
        self.cursor.execute("""
        SELECT id, task, priority, done, deadline, date_finished
        FROM tasks
        ORDER BY priority DESC
        """)

        return self.cursor.fetchall()

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

            db_id = input(message)

            if self._validate_int(db_id):
                return self.lookup_table[int(db_id)]

    def _write(self, command: str, values: tuple) -> None:
        self.cursor.execute(command, values)
        self.connection.commit()

    def _get_task_details(self) -> tuple:
        task = input("Enter task: ")
        priority = input("Priority? (y/n): ").lower()
        has_deadline = input("Deadline? (y/n): ").lower()

        if has_deadline == 'y':
            deadline = input("Enter deadline (yyyy-mm-dd): ")
        else:
            deadline = None

        return task, (1 if priority == "y" else 0), deadline

    def _return_lookup_table(self) -> dict:
        tasks = self._get_tasks()
        lookup_table = {}

        for i, (db_id, _, _, _, _, _) in enumerate(tasks, start=1):
            lookup_table[i] = db_id

        return lookup_table

    def print_tasks(self) -> None:
        tasks = self._get_tasks()

        for i, (_, task, priority, done, deadline, date_finished) in enumerate(tasks, start=1):
            if done:
                print(f"{i}. {task} - Done on {date_finished}.")
            else:
                print(f"{i}. {"[PRIORITY] " if priority else ""}{task} - Not done. {"Deadline: " if deadline else ""}{deadline if deadline else ""}")

    def mark_task_as_done(self) -> None:
        db_id = self._get_id("Enter ID of task to mark as done: ")

        self._write("""
        UPDATE tasks
        SET done = TRUE,
        date_finished = DATE(NOW())
        WHERE id = %s
        """, 
        (db_id,))

    def add_task(self) -> None:
        task, priority, deadline = self._get_task_details()

        self._write("""
        INSERT INTO tasks (task, priority, deadline)
        VALUES (%s, %s, %s)
        """,
        (task, priority, deadline))

        self.lookup_table = self._return_lookup_table()

    def modify_task(self) -> None:
        db_id = self._get_id("Enter number of task you wish to modify: ")

        task, priority, deadline = self._get_task_details()

        self._write("""
        UPDATE tasks
        SET task = %s,
        priority = %s,
        deadline = %s
        WHERE id = %s
        """,
        (task, priority, deadline, db_id))

        self.lookup_table = self._return_lookup_table()

    def remove_task(self) -> None:
        db_id = self._get_id("Enter number of task you wish to remove: ")

        self._write("""
        DELETE FROM tasks
        WHERE id = %s
        """,
        (db_id,))

        self.lookup_table = self._return_lookup_table()