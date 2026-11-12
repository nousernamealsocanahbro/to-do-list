from database import Database

options = ['View tasks', 'Mark task as done', 'Add task', 'Modify task', 'Remove task', 'Exit']

def _validate_int(message: str) -> bool:
    try:
        int(message)

        return True
    except ValueError as e:
        print(e)

        return False

def get_int(message: str) -> int:
    while True:
        number = input(message)

        if _validate_int(number):
            return int(number)
        
def main() -> None:
    db = Database()

    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = get_int("Enter choice: ")
            
            if choice == 1:
                db.print_tasks()
                input("Press enter to continue... ")
            elif choice == 2:
                db.mark_task_as_done()
                print("Task marked as done. ")
                input("Press enter to continue... ")
            elif choice == 3:
                db.add_task()
                print("Task added. ")
                input("Press enter to continue... ")
            elif choice == 4:
                db.modify_task()
                print("Task modifed. ")
                input("Press enter to continue... ")
            elif choice == 5:
                db.remove_task()
                print("Task removed. ")
                input("Press enter to continue... ")
            elif choice == 6:
                print("Bye") # mysql says this when you exit it and i think its funny
                break
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()