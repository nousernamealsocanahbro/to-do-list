def view_tasks(file):
    with open(file, 'r') as f:
        for i, v in enumerate(f):
            print(i+1, v, end="")

def add_task(file):
    task = input("Input task: ")
    
    with open(file, 'a') as f:
        f.write(f'{task}\n')
        
        print(f"{task} has been added")

def remove_task(file):
    with open(file, 'r') as f:
        tasks = list(f)
        
        for i, v in enumerate(tasks, 1):
            print(i, v, end="\n")
        
        try:
            task_number = int(input("Input task to remove: "))
            
            if task_number < 1:
                print("Task number must be a positive integer, please try again.")
            else:
                tasks.pop(task_number-1)
            
                with open(file, 'w') as ff:
                    ff.writelines(tasks)
        except ValueError as e:
            print(e)
        
def main():
    file_name = input("Input name for file without file extension: ") + '.txt'
    file = open(file_name, 'a')
    file.close()
    
    while True:
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Exit")
        
        try:
            choice = int(input("Enter choice: "))
            
            if choice < 1 or choice > 4:
                print("Choice must be 1-4, please try again.")
            else:
                if choice == 1:
                    view_tasks(file_name)
                elif choice == 2:
                    add_task(file_name)
                elif choice == 3:
                    remove_task(file_name)
                else:
                    break
        except ValueError as e:
            print(e)

main()