import sqlite3
from datetime import datetime
from src.habit import Habit
from src.periodicity import Periodicity


class SQLiteStorage:
    """handles saving and loading habit data using SQLite database"""
    def __init__(self, db_path: str = "data/habittracker.db"):
        self.db_path = db_path
        self._create_database()

    def _create_database(self) -> None:
        """Creates the database tables if they do not already exist."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )
                """
            )

            connection.commit()

    def save_habit(self, habit: Habit) -> int:
        """Saves a new habit and returns its databade ID."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO habits (name, description, periodicity, created_at) VALUES (?,?,?,?)",
                (habit.name, getattr(habit, "description", None), habit.periodicity.value if isinstance(habit.periodicity, Periodicity) else str(habit.periodicity), habit.created_at.isoformat()),
            )
            habit_id = cursor.lastrowid

            # save any provided completions
            for dt in getattr(habit, "completed_dates", []):
                cursor.execute(
                    "INSERT INTO completions (habit_id, completed_at) VALUES (?,?)",
                    (habit_id, dt.isoformat()),
                )

            connection.commit()
            return habit_id

    def save_completion(self, habit_id: int, completed_at: datetime) -> None:
        """Records a completion for a specific habit."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO completions (habit_id, completed_at)
                Values (?,?)
            """, (habit_id, completed_at.isoformat()))
            
            connection.commit()
    def delete_habit(self, habit_id: int) -> None:
        """Deletes a habit and its completions from the records."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM completions WHERE habit_id = ?",
                (habit_id,),
            )
            cursor.execute(
                "DELETE FROM habits WHERE id = ?", 
                (habit_id,)
            )
            
            connection.commit()
                    
        
        
