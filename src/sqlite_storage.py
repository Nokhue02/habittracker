import sqlite3
from pathlib import Path
from datetime import datetime

from src.habit import Habit
from src.periodicity import Periodicity


class SQLiteStorage:
    """Handles saving and loading habits using SQLite."""

    def __init__(self, db_path="data/habittracker.db"):
        self.db_path = db_path

        Path(self.db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_database()


    def _create_database(self):

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)


            cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                completed_at TEXT NOT NULL,

                FOREIGN KEY(habit_id)
                REFERENCES habits(id)
                ON DELETE CASCADE
            )
            """)

            connection.commit()


    def save_habit(self, habit: Habit):

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.cursor()


            cursor.execute(
                """
                INSERT INTO habits
                (name, periodicity, created_at)

                VALUES (?, ?, ?)
                """,

                (
                    habit.name,
                    habit.periodicity.value,
                    habit.created_at.isoformat()
                )
            )


            habit.id = cursor.lastrowid

            connection.commit()


    def load_habits(self):

        habits = []


        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.cursor()


            cursor.execute(
                """
                SELECT id,
                name,
                periodicity,
                created_at

                FROM habits
                """
            )


            rows = cursor.fetchall()


            for row in rows:


                cursor.execute(
                    """
                    SELECT completed_at

                    FROM completions

                    WHERE habit_id = ?

                    """,
                    (row[0],)
                )


                completion_rows = cursor.fetchall()


                completed_dates = [
                    datetime.fromisoformat(
                        c[0]
                    ).date()

                    for c in completion_rows
                ]


                habit = Habit(

                    id=row[0],

                    name=row[1],

                    periodicity=Periodicity(row[2]),

                    created_at=datetime.fromisoformat(
                        row[3]
                    ),

                    completed_dates=completed_dates

                )


                habits.append(habit)


        return habits



    def save_completion(
        self,
        habit_id,
        completed_at
    ):


        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.cursor()


            cursor.execute(

                """
                INSERT INTO completions

                (habit_id, completed_at)

                VALUES (?,?)

                """,

                (
                    habit_id,
                    completed_at.isoformat()
                )

            )


            connection.commit()



    def delete_habit(self, habit_id):

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.cursor()


            cursor.execute(

                """
                DELETE FROM habits

                WHERE id = ?

                """,

                (habit_id,)

            )


            connection.commit()