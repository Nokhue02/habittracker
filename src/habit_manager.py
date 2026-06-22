from datetime import datetime

from src.habit import Habit
from src.periodicity import Periodicity
from src.sqlite_storage import SQLiteStorage



class HabitManager:

    def __init__(self):

        self.storage = SQLiteStorage()

        self.habits = self.storage.load_habits()



    def add_habit(self, name):

        if not name.strip():

            print("Habit name cannot be empty.")
            return


        habit = Habit(

            id=None,

            name=name,

            periodicity=Periodicity.DAILY

        )


        self.storage.save_habit(habit)

        self.habits.append(habit)


        print(
            f"Habit '{name}' added."
        )



    def view_habits(self):

        self.habits = self.storage.load_habits()


        if not self.habits:

            print("No habits found.")
            return


        print("\n=== Your Habits ===")


        for habit in self.habits:


            status = (

                "Completed"

                if habit.get_completion_count() > 0

                else "Not completed"

            )


            print(

                f"{habit.id}. "
                f"{habit.name} - "
                f"{status}"

            )




    def complete_habit(self, habit_id):


        habit = next(

            (
                h for h in self.habits
                if h.id == habit_id
            ),

            None

        )


        if habit is None:

            print("Invalid habit.")
            return False



        habit.check_off()


        self.storage.save_completion(

            habit.id,

            datetime.now()

        )


        print(

            f"Habit '{habit.name}' completed."

        )


        return True




    def delete_habit(self, habit_id):


        self.storage.delete_habit(habit_id)


        self.habits = self.storage.load_habits()


        print("Habit deleted.")




    def analyse_habits(self):
        from src.habit_analysis import (
        calculate_longest_streak_overall,
        get_current_streaks
        )


        self.habits = self.storage.load_habits()


        if not self.habits:
            print("No habits to analyse.")
            return



        total = len(self.habits)


        completed = sum(
        1
        for habit in self.habits
        if habit.get_completion_count() > 0
        )


        print("\n=== Habit Analysis ===")

        print(
        f"Total habits: {total}"
        )

        print(
        f"Completed habits: {completed}"
        )

        print(
        f"Incomplete habits: {total-completed}"
        )


        longest = calculate_longest_streak_overall(
        self.habits
        )


        print(
        f"\nLongest streak overall: {longest} days"
        )


        print("\nCurrent streaks:")


        streaks = get_current_streaks(
        self.habits
        )


        for item in streaks:
            print(
            f"{item['habit']}: "
            f"{item['streak']} days"
            )