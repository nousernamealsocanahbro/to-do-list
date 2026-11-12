from database import Database

options = ['View tasks', 'Mark task as done', 'Add task', 'Modify task', 'Remove task', 'Exit']
        
def main() -> None:
    db = Database()

    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                db.print_tasks()
                input("Press enter to continue... ")
            elif choice == 2:
                db.mark_task_as_done()
                input("Task marked as done. ")
            elif choice == 3:
                db.add_task()
                input("Task added. ")
            elif choice == 4:
                db.modify_task()
                input("Task modifed. ")
            elif choice == 5:
                db.remove_task()
                input("Task removed. ")
            elif choice == 6:
                print("Bye") # mysql says this when you exit it and i think its funny
                break
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()