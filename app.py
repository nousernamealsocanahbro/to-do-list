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

    db.create_table()

    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = get_int("Enter choice: ")

            match choice:
                case 1:
                    db.print_tasks()
                case 2:
                    db.mark_task_as_done()
                    print("Task marked as done.")
                case 3:
                    db.add_task()
                    print("Task added.")
                case 4:
                    db.modify_task()
                    print("Task modified.")
                case 5:
                    db.remove_task()
                    print("Task removed.")
                case 6:
                    print("Bye")
                    break            

            input("Press enter to continue...")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()