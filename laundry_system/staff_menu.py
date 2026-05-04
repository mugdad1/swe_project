from __future__ import annotations
from classes import Staff, Task
from utils import (
    find_staff_by_id,
    get_staff_tasks,
    find_task_by_id,
    clear_screen,
    pause,
    show_message,
)
from data import staff


def staff_login() -> None:
    clear_screen()
    print("\n=== Staff Login ===")
    try:
        staff_id: int = int(input("Enter your staff ID: "))
    except ValueError:
        show_message("Invalid ID! Enter a number.", wait_time=2)
        return

    staff_member: Staff | None = find_staff_by_id(staff_id)

    if staff_member:
        print(f"Welcome, {staff_member.name}!")
        pause()
        staff_dashboard(staff_member)
    else:
        show_message("Staff ID not found!", wait_time=2)


def staff_dashboard(staff_member: Staff) -> None:
    while True:
        clear_screen()
        print(f"\n=== Staff Dashboard ({staff_member.name}) ===")
        print("1. View My Tasks")
        print("2. Update Task Status")
        print("3. Add Notes to Task")
        print("4. Logout")

        choice: str = input("\nEnter your choice: ")

        if choice == "1":
            view_tasks(staff_member)
        elif choice == "2":
            update_task_status(staff_member)
        elif choice == "3":
            add_task_notes(staff_member)
        elif choice == "4":
            print("Logging out...")
            pause()
            break
        else:
            show_message("Invalid choice!", wait_time=1)


def view_tasks(staff_member: Staff) -> None:
    clear_screen()
    print("\n=== Your Tasks ===")
    tasks: list[Task | None] = get_staff_tasks(staff_member.staff_id)

    if not tasks:
        show_message("You have no tasks assigned.", wait_time=2)
        return

    for task in tasks:
        if task:
            print(task)

    pause()


def update_task_status(staff_member: Staff) -> None:
    clear_screen()
    print("\n=== Update Task Status ===")

    tasks = get_staff_tasks(staff_member.staff_id)
    if not tasks:
        show_message("You have no tasks!", wait_time=2)
        return

    try:
        task_id: int = int(input("Enter task ID: "))
    except ValueError:
        show_message("Invalid task ID! Enter a number.", wait_time=2)
        return

    task: Task | None = find_task_by_id(task_id)

    if task and task_id in staff_member.assigned_tasks:
        print("\nSelect new status:")
        print("1. Not Started")
        print("2. In Progress")
        print("3. Done")

        status_choice: str = input("\nEnter your choice: ")

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


def add_task_notes(staff_member: Staff) -> None:
    clear_screen()
    print("\n=== Add Notes to Task ===")

    tasks = get_staff_tasks(staff_member.staff_id)
    if not tasks:
        show_message("You have no tasks!", wait_time=2)
        return

    try:
        task_id: int = int(input("Enter task ID: "))
    except ValueError:
        show_message("Invalid task ID! Enter a number.", wait_time=2)
        return

    task: Task | None = find_task_by_id(task_id)

    if task and task_id in staff_member.assigned_tasks:
        notes: str = input("Enter notes: ")
        task.notes = notes
        show_message("Notes added successfully!", wait_time=2)
    else:
        show_message("Task not found or not assigned to you!", wait_time=2)
