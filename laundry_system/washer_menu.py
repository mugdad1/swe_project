from utils import find_washer_by_id, get_washer_tasks, find_task_by_id, clear_screen, pause, show_message
from data import washers


def washer_login():
    """Login as a washer"""
    clear_screen()
    print("\n=== Washer Login ===")
    washer_id = int(input("Enter your washer ID: "))

    washer = find_washer_by_id(washer_id)

    if washer:
        print(f"Welcome, {washer.name}!")
        pause()
        washer_dashboard(washer)
    else:
        show_message("Washer ID not found!", wait_time=2)


def washer_dashboard(washer):
    """Washer main menu"""
    while True:
        clear_screen()
        print(f"\n=== Washer Dashboard ({washer.name}) ===")
        print("1. View My Tasks")
        print("2. Update Task Status")
        print("3. Add Notes to Task")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_tasks(washer)
        elif choice == "2":
            update_task_status(washer)
        elif choice == "3":
            add_task_notes(washer)
        elif choice == "4":
            print("Logging out...")
            pause()
            break
        else:
            show_message("Invalid choice!", wait_time=1)


def view_tasks(washer):
    """View all tasks assigned to the washer"""
    clear_screen()
    print("\n=== Your Tasks ===")
    tasks = get_washer_tasks(washer.washer_id)

    if not tasks:
        show_message("You have no tasks assigned.", wait_time=2)
        return

    for task in tasks:
        print(task)

    pause()


def update_task_status(washer):
    """Update the status of a task"""
    clear_screen()
    print("\n=== Update Task Status ===")
    task_id = int(input("Enter task ID: "))

    task = find_task_by_id(task_id)

    if task and task_id in washer.assigned_tasks:
        print("\nSelect new status:")
        print("1. Not Started")
        print("2. In Progress")
        print("3. Done")

        status_choice = input("\nEnter your choice: ")

        if status_choice == "1":
            task.status = "Not Started"
        elif status_choice == "2":
            task.status = "In Progress"
        elif status_choice == "3":
            task.status = "Done"
        else:
            show_message("Invalid choice!", wait_time=1)
            return

        show_message(f"Task status updated to: {task.status}", wait_time=2)
    else:
        show_message("Task not found or not assigned to you!", wait_time=2)


def add_task_notes(washer):
    """Add notes to a task"""
    clear_screen()
    print("\n=== Add Notes to Task ===")
    task_id = int(input("Enter task ID: "))

    task = find_task_by_id(task_id)

    if task and task_id in washer.assigned_tasks:
        notes = input("Enter notes: ")
        task.notes = notes
        show_message("Notes added successfully!", wait_time=2)
    else:
        show_message("Task not found or not assigned to you!", wait_time=2)
