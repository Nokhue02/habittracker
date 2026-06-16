class HabitManager:
    """Manages the creation, deletion, completion, and listing of habits."""

    def __init__(self):
        self.habits = []

    def add_habit(self, name):
        if not name.strip():
            print("Habit name cannot be empty.")
            return

        self.habits.append({
            "name": name,
            "completed": False
        })
        print(f"Habit '{name}' added.")
        

    def view_habits(self):
        if not self.habits:
            print("No habits found.")
            return

        print("\n=== Your Habits ===")
        for index, habit in enumerate(self.habits, start=1):
            status = "Completed" if habit["completed"] else "Not completed"
            print(f"{index}. {habit['name']} - {status}")

    def complete_habit(self, habit_id: int):
        if 1 <= habit_id <= len(self.habits):
            self.habits[habit_id - 1]["completed"] = True
            print(f"Habit '{self.habits[habit_id - 1]['name']}' completed.")
            return True

        print("Invalid habit number.")
        return False

    def delete_habit(self, habit_id: int):
        if 1 <= habit_id <= len(self.habits):
            removed = self.habits.pop(habit_id - 1)
            print(f"Habit '{removed['name']}' deleted.")
            return True

        print("Invalid habit number.")
        return False

    def analyse_habits(self):
        if not self.habits:
            print("No habits to analyse.")
            return

        total_habits = len(self.habits)
        completed_habits = sum(1 for habit in self.habits if habit["completed"])
        incomplete_habits = total_habits - completed_habits

        print("\n=== Habit Analysis ===")
        print(f"Total habits: {total_habits}")
        print(f"Completed habits: {completed_habits}")
        print(f"Incomplete habits: {incomplete_habits}")