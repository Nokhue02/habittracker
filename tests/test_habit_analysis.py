import pytest
from datetime import datetime, timedelta
from src.habit import Habit
from src.periodicity import Periodicity
from src.habit_analysis import (
    get_all_habits,
    filter_habits_by_periodicity,
    calculate_longest_streak_for_habit,
    calculate_current_streak_for_habit,
    calculate_longest_streak_overall
)

@pytest.fixture
def sample_habits():
    """Fixture to provide habit data for testing."""
    today = datetime.now().date()
    
    # Habit 1: Daily, 3-day streak
    h1 = Habit(id=1, name="Read", periodicity=Periodicity.DAILY)
    h1.completed_dates = [
        today - timedelta(days=4), 
        today - timedelta(days=3), 
        today - timedelta(days=2)
    ]
    
    # Habit 2: Daily, 2-day current streak
    h2 = Habit(id=2, name="Walk", periodicity=Periodicity.DAILY)
    h2.completed_dates = [
        today - timedelta(days=1), 
        today
    ]
    
    return [h1, h2]

def test_get_all_habits(sample_habits):
    assert len(get_all_habits(sample_habits)) == 2

def test_filter_habits_by_periodicity(sample_habits):
    daily_habits = filter_habits_by_periodicity(sample_habits, Periodicity.DAILY)
    weekly_habits = filter_habits_by_periodicity(sample_habits, Periodicity.WEEKLY)
    
    assert len(daily_habits) == 2
    assert len(weekly_habits) == 0

def test_calculate_longest_streak_for_habit(sample_habits):
    h1 = sample_habits[0] # Has a 3-day streak
    assert calculate_longest_streak_for_habit(h1) == 3

def test_calculate_current_streak_for_habit(sample_habits):
    h2 = sample_habits[1] # Completed yesterday and today
    assert calculate_current_streak_for_habit(h2) == 2
    
def test_calculate_longest_streak_overall(sample_habits):
    assert calculate_longest_streak_overall(sample_habits) == 3