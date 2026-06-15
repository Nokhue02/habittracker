from src.periodicity import Periodicity


def get_all_habits(habits: list) -> list:
    """Returns a list of all habits"""
    return habits


def filter_habits_by_periodicity(habits: list, periodicity: Periodicity) -> list:
    """Filters habits by periodicity"""
    return list(filter(lambda habit: habit.periodicity == periodicity, habits))


def calculate_longest_streak_for_habit(habit) -> int:
    """Calculates the longest streak for a habit"""
    return habit.get_completion_count()  # Placeholder implementation, replace with actual streak calculation logic


def calculate_longest_streak_overall(habits: list) -> int:
    """Calculates the longest streak overall across all habits"""
    streaks = map(lambda habit: calculate_longest_streak_for_habit(habit), habits)
    return max(streaks, default=0)


def get_current_streaks(habits: list) -> list:
    """Returns a list of the current streak for each habit"""
    return list(map(lambda habit: calculate_longest_streak_for_habit(habit), habits))

