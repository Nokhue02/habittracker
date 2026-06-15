import sqlite3
from datetime import datetime
from habit_analysis.habit import Habit
from habit_analysis.periodicity import Periodicity


class SQLiteStorage:
    """handles saving and loading habit data using SQLite database"""
    def __init__(self, db_path: str = "data/habittracker.db"):
        self.db_path = db_path
        self._create_database()

    def _create_database(self) -> None:
        """Creates the database tables if they do not already exist."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
           

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id) 
            )
            """)
        connection.commit()

    def save_habit(self, habit: Habit) -> int:
        """Saves a new habit and returns its databade ID."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            
            cursor.execute("SELECT id name, periodicity, created_at FROM habits")
            habit_rows= cursor.fetchall()

            habits = []

            for row in habit_rows:
                habit_id, name, periodicty, created_at = row

                cursor.execute("""
                     SELECT completed_at 
                     FROM completions 
                     WHERE habit_id = ?
                """, (habit_id,))
                completion_rows = cursor.fetchall()

                completed_dates = [
                    datetime.fromisoformat(date[0]) 
                    for  date in completion_rows
                ]
                
                habit= Habit(
                    id=habit_id,
                    name=name,
                    periodicity=Periodicity(periodicty)
                    created_at=datetime.fromisoformat(created_at),
                    completed_dates=completed_dates
                )
                habits.append(habit)
    
            return habits 

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
                "DELETE FROM habit_completions WHERE habit_id = ?", 
                (habit_id,)
            )
            cursor.execute(
                "DELETE FROM habits WHERE id = ?", 
                (habit_id,)
            )
            
            connection.commit()
                    
        
        
