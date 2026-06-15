import pytest
from src.habit import Habit
from src.periodicity import Periodicity

def test_habit_creation():
    habit = Habit(
        id=1,
        name="Exercise",
        periodicity=Periodicity.DAILY
    )
    assert habt.id==1
    assert habit.name == "Exercise"
    assert habit.periodicity == Periodicity.DAILY

def test_habit_check_off():
    habit = Habit(
        id=1,
        name="Exercise",
        periodicity=Periodicity.DAILY
    )
    habit.check_off()
    assert len(habit.completed_dates) == 1

def test_habit_completion_count():
    habit = Habit(
        id=1,
        name="Exercise",
        periodicity=Periodicity.DAILY
    )
    
    habit.check_off()
    habit.check_off()  
    
    assert habit.get_completion_count() == 2
    
