from src.habit import Habit
from src.periodicity import Periodicity


class HabitManager:
    """Manages the creation, deletion, completion, and listing of habit."""
    
    def __init__(self):
        self.habits = []
    
    def add_habit(self, habit: Habit) -> None:
        """Adds a new habit to the habit list."""
        self.habits.append(habit)

    def delete_habit(self, habit_id: int) -> None:
        """Deletes a habit by its unique identifier."""
        self.habits = [habit for habit in self.habits if habit.id != habit_id]

    
    def find_habit_by_id(self, habit_id: int):
        """Finds and returns a habit by its unique identifier."""
        for habit in self.habits:
            if habit.id == habit_id:
                return habit  
        return None

    def complete_habit(self, habit_id: int) -> bool:
        """Marks a habit as completed and returns True if the habit was found."""
        habit = self.find_habit_by_id(habit_id)
        if habit is None:
            return False

        habit.check_off()
        return True

    def get_all_habits(self) -> list:
        """Returns a list of all current habits."""
        return list(self.habits)

    

      
    