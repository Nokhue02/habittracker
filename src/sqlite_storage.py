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



    def _get_connection(self):

        connection = sqlite3.connect(
            self.db_path
        )

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection



    def _create_database(self):

        with self._get_connection() as connection:

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

                habit_id INTEGER NOT NULL,

                completed_at TEXT NOT NULL,


                FOREIGN KEY(habit_id)

                REFERENCES habits(id)

                ON DELETE CASCADE

            )
            """)



            connection.commit()




    def save_habit(self, habit: Habit):

        with self._get_connection() as connection:

            cursor = connection.cursor()


            cursor.execute(

                """
                INSERT INTO habits

                (
                    name,
                    periodicity,
                    created_at
                )

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


        with self._get_connection() as connection:

            cursor = connection.cursor()


            cursor.execute(

                """
                SELECT

                id,
                name,
                periodicity,
                created_at


                FROM habits

                ORDER BY id

                """

            )


            rows = cursor.fetchall()



            for row in rows:


                cursor.execute(

                    """
                    SELECT completed_at

                    FROM completions

                    WHERE habit_id = ?

                    ORDER BY completed_at

                    """,

                    (row[0],)

                )


                completion_rows = cursor.fetchall()



                completed_dates = [

                    datetime.fromisoformat(

                        item[0]

                    ).date()


                    for item in completion_rows

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


        with self._get_connection() as connection:

            cursor = connection.cursor()



            cursor.execute(

                """
                INSERT INTO completions

                (
                    habit_id,
                    completed_at
                )

                VALUES (?,?)

                """,

                (

                    habit_id,

                    completed_at.isoformat()

                )

            )


            connection.commit()






    def completion_exists(
        self,
        habit_id,
        completion_date
    ):

        with self._get_connection() as connection:

            cursor = connection.cursor()



            cursor.execute(

                """
                SELECT 1

                FROM completions

                WHERE habit_id = ?

                AND DATE(completed_at) = ?

                """,

                (

                    habit_id,

                    completion_date

                )

            )



            return cursor.fetchone() is not None







    def habit_exists(
        self,
        habit_id
    ):


        with self._get_connection() as connection:

            cursor = connection.cursor()



            cursor.execute(

                """
                SELECT 1

                FROM habits

                WHERE id = ?

                """,

                (habit_id,)

            )


            return cursor.fetchone() is not None







    def delete_habit(
        self,
        habit_id
    ):


        with self._get_connection() as connection:

            cursor = connection.cursor()



            cursor.execute(

                """
                DELETE FROM habits

                WHERE id = ?

                """,

                (habit_id,)

            )


            connection.commit()