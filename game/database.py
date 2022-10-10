import sqlite3
from typing import List, Tuple

TABLE_NAME = 'leaderboard'


class DatabaseAPI:
    # TODO: Rewrite using WITH statement
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self._create_table()

    def add_new_result(self, name: str, score: int):
        cursor = self.connection.cursor()
        sql_command = f'''INSERT INTO {TABLE_NAME}
        (name, score) VALUES ('{name}', '{score}')'''

        cursor.execute(sql_command)
        self.connection.commit()
        cursor.close()

    def get_from_table(self) -> List[Tuple[str, int]]:
        cursor = self.connection.cursor()
        sql_command = f'''SELECT name, score
        FROM {TABLE_NAME}'''

        cursor.execute(sql_command)
        data = cursor.fetchall()
        cursor.close()
        return data

    def delete_from_table(self):
        cursor = self.connection.cursor()
        sql_command = f'''DELETE FROM {TABLE_NAME}'''
        cursor.execute(sql_command)
        self.connection.commit()
        cursor.close()

    def _create_table(self):
        cursor = self.connection.cursor()
        sql_command = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             score INTEGER NOT NULL );'''

        cursor.execute(sql_command)
        cursor.close()
