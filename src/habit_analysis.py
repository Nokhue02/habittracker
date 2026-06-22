from datetime import timedelta
from src.periodicity import Periodicity


def get_all_habits(habits: list) -> list:
    """
    Returns all habits.
    """
    return habits



def filter_habits_by_periodicity(
    habits: list,
    periodicity: Periodicity
) -> list:
    """
    Returns habits matching a periodicity.
    """

    return [
        habit
        for habit in habits
        if habit.periodicity == periodicity
    ]



def calculate_longest_streak_for_habit(habit) -> int:
    """
    Calculates the longest consecutive completion streak.
    """

    if not habit.completed_dates:
        return 0


    dates = sorted(
        habit.completed_dates
    )


    longest_streak = 1

    current_streak = 1


    for i in range(1, len(dates)):


        difference = (
            dates[i] - dates[i-1]
        )


        if difference == timedelta(days=1):

            current_streak += 1


        else:

            current_streak = 1



        if current_streak > longest_streak:

            longest_streak = current_streak



    return longest_streak




def calculate_current_streak_for_habit(habit) -> int:
    """
    Calculates the current active streak.
    """

    if not habit.completed_dates:

        return 0



    dates = sorted(
        habit.completed_dates,
        reverse=True
    )


    streak = 1


    for i in range(len(dates)-1):


        difference = (
            dates[i] - dates[i+1]
        )


        if difference == timedelta(days=1):

            streak += 1


        else:

            break



    return streak




def calculate_longest_streak_overall(
    habits: list
) -> int:
    """
    Returns the highest streak among all habits.
    """


    if not habits:

        return 0



    return max(

        calculate_longest_streak_for_habit(habit)

        for habit in habits

    )




def get_current_streaks(
    habits: list
) -> list:
    """
    Returns current streak for every habit.
    """


    return [

        {
            "habit": habit.name,

            "streak": calculate_current_streak_for_habit(habit)

        }

        for habit in habits

    ]