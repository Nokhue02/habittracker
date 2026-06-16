from src.habit_manager import HabitManager


class CLI:
    def __init__(self):
        self.manager = HabitManager()

    def show_menu(self):
        print("=== Habit Tracker ===")
        print("1. View Habits")
        print("2. Add Habit")
        print("3. Complete Habit")
        print("4. Delete Habit")
        print("5. Analyse Habits")
        print("6. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                self.manager.view_habits()

            elif choice == "2":
                name = input("Habit name: ")
                self.manager.add_habit(name)

            elif choice == "3":
                try:
                    hid = int(input("Habit id to complete: "))
                    self.manager.complete_habit(hid)
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "4":
                try:
                    hid = int(input("Habit id to delete: "))
                    self.manager.delete_habit(hid)
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "5":
                self.manager.analyse_habits()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose 1-6.")