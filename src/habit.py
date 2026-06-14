from datetime import datetime
from periodicity import Periodicity


class Habit:
    """Represents the Habit the user wants to track"""

    def __init__(self, id: int, name: str, periodicity: Periodicity, created_at=None, completed_dates=None):
        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at if created_at is not None else datetime.now()
        self.completed_dates = completed_dates if completed_dates is not None else []
    def check_off(self) -> None:
        """Marks the habit as completed for the current date"""
        today = datetime.now().date()
        if today not in self.completed_dates:
            self.completed_dates.append(today)
    def get_completion_count(self) -> int:
        """Returns the number of completed dates for the habit"""
        return len(self.completed_dates)
    def __str__(self) -> str:
        return f"Habit(id={self.id}, name='{self.name}', periodicity='{self.periodicity.value}', created_at='{self.created_at}', completed_dates={self.completed_dates})"