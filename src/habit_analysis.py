from datetime import timedelta, datetime
from functools import reduce
from src.periodicity import Periodicity


def get_all_habits(habits: list) -> list:
    """
    Returns all habits.
    """
    return habits


def filter_habits_by_periodicity(habits: list, periodicity: Periodicity) -> list:
    """
    Returns habits matching a periodicity using functional filtering.
    """
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def _get_allowed_gap(periodicity: Periodicity) -> timedelta:
    """
    Helper function mapping periodicity to the maximum allowed time gap to maintain a streak.
    """
    gaps = {
        Periodicity.DAILY: timedelta(days=1),
        Periodicity.WEEKLY: timedelta(days=7),
        Periodicity.MONTHLY: timedelta(days=31), 
        Periodicity.YEARLY: timedelta(days=365)
    }
    return gaps.get(periodicity, timedelta(days=1))


def calculate_longest_streak_for_habit(habit) -> int:
    """
    Calculates the longest consecutive completion streak using a functional reducer.
    """
    if not habit.completed_dates:
        return 0

    # Sort dates and remove duplicates if any exist
    dates = sorted(set(habit.completed_dates))
    allowed_gap = _get_allowed_gap(habit.periodicity)

    def streak_reducer(acc, current_date):
        current_streak, max_streak, prev_date = acc
        
        if prev_date is None:
            return (1, 1, current_date)
        
        diff = current_date - prev_date
        
        # If the gap is within the allowed periodicity threshold, increment streak
        if timedelta(days=1) <= diff <= allowed_gap:
            new_streak = current_streak + 1
            return (new_streak, max(max_streak, new_streak), current_date)
        elif diff > allowed_gap:
            # Streak broken, reset to 1
            return (1, max_streak, current_date)
        else:
            # Same day completion, do not increment but keep the streak alive
            return (current_streak, max_streak, current_date)

    # reduce returns a tuple: (final_current_streak, final_max_streak, last_date)
    _, longest_streak, _ = reduce(streak_reducer, dates, (0, 0, None))
    
    return longest_streak


def calculate_current_streak_for_habit(habit) -> int:
    """
    Calculates the current active streak functionally.
    """
    if not habit.completed_dates:
        return 0

    # Sort dates from newest to oldest
    dates = sorted(set(habit.completed_dates), reverse=True)
    allowed_gap = _get_allowed_gap(habit.periodicity)
    today = datetime.now().date()

    # If the most recent completion is older than the allowed gap from today, the current streak is dead (0)
    if (today - dates[0]) > allowed_gap:
        return 0

    def current_streak_reducer(acc, current_date):
        streak, prev_date, keep_counting = acc
        
        if not keep_counting:
            return acc
            
        if prev_date is None:
            return (1, current_date, True)
            
        diff = prev_date - current_date
        
        # As long as the gap going backward is valid, keep incrementing
        if timedelta(days=1) <= diff <= allowed_gap:
            return (streak + 1, current_date, True)
        else:
            # Gap is too large, streak broken, stop counting
            return (streak, current_date, False)

    final_streak, _, _ = reduce(current_streak_reducer, dates, (0, None, True))
    
    return final_streak


def calculate_longest_streak_overall(habits: list) -> int:
    """
    Returns the highest streak among all habits using functional mapping.
    """
    if not habits:
        return 0
        
    streaks = list(map(calculate_longest_streak_for_habit, habits))
    
    return max(streaks) if streaks else 0


def get_current_streaks(habits: list) -> list:
    """
    Returns the current streak for every habit using functional mapping.
    """
    def format_streak(habit):
        return {
            "habit": habit.name,
            "streak": calculate_current_streak_for_habit(habit)
        }
        
    return list(map(format_streak, habits))