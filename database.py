'''
it is 12/11/26 at 0039
add a mark as done function
i want to sleep
'''

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = self._connect_to_db()
        self.cursor = self.connection.cursor()

    def _connect_to_db(self):
        return mysql.connector.connect(
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASSWORD'],
            database = os.environ['DB_NAME'],
            host = os.environ['DB_HOST'],
        )

    def _get_tasks(self) -> list:
        self.cursor.execute("SELECT id, task, done FROM tasks")

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
                return db_id

    def _write(self, command: str, values: tuple) -> None:
        self.cursor.execute(command, values)
        self.connection.commit()

    def _get_task_details(self) -> str:
        task = input("Enter task: ")

        return task

    def print_tasks(self):
        tasks = self._get_tasks()

        for i, (id, task, done) in enumerate(tasks):
            print(f"{id}. {task} [{"Done" if done else "Not done"}]")

    def mark_task_as_done(self):
        db_id = self._get_id("Enter ID of task to mark as done: ")

        self._write("""
        UPDATE tasks
        SET done = TRUE
        WHERE id = %s
        """, 
        (db_id,))

    def add_task(self):
        task = self._get_task_details()

        self._write("""
        INSERT INTO tasks (task)
        VALUES (%s)
        """,
        (task,))

    def modify_task(self):
        db_id = self._get_id("Enter ID of task you wish to remove: ")

        task = self._get_task_details()

        self._write("""
        UPDATE tasks
        SET task = %s
        WHERE id = %s
        """,
        (task, db_id))

    def remove_task(self):
        db_id = self._get_id("Enter ID of task you wish to remove: ")

        self._write("""
        DELETE FROM tasks
        WHERE id = %s
        """,
        (db_id,))