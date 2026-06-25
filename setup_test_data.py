from datetime import datetime, timedelta
from src.habit import Habit
from src.periodicity import Periodicity
from src.sqlite_storage import SQLiteStorage

def generate_test_data():
    storage = SQLiteStorage()
    now = datetime.now()
    
    # Define 5 Predefined Habits (Daily & Weekly)
    predefined_habits = [
        {"name": "Pray 3 times", "periodicity": Periodicity.DAILY},
        {"name": "Read 10 Pages", "periodicity": Periodicity.DAILY},
        {"name": "Morning Stretch", "periodicity": Periodicity.DAILY},
        {"name": "Grocery Shopping", "periodicity": Periodicity.WEEKLY},
        {"name": "Call Parents", "periodicity": Periodicity.WEEKLY}
    ]
    
    print("Injecting predefined habits...")
    for h_data in predefined_habits:
        # Create habit artificially dated 4 weeks ago
        created_date = now - timedelta(days=28)
        habit = Habit(
            id=None, 
            name=h_data["name"], 
            periodicity=h_data["periodicity"], 
            created_at=created_date
        )
        storage.save_habit(habit)
        
        # Generate 4 weeks of completion data
        if habit.periodicity == Periodicity.DAILY:
            # Simulate a 20-day streak out of 28 days
            for i in range(20):
                completion_date = now - timedelta(days=i)
                storage.save_completion(habit.id, completion_date)
                
        elif habit.periodicity == Periodicity.WEEKLY:
            # Simulate 4 weekly completions
            for i in range(4):
                completion_date = now - timedelta(weeks=i)
                storage.save_completion(habit.id, completion_date)

    print("Test fixture data successfully loaded into the database!")

if __name__ == "__main__":
    generate_test_data()