from __future__ import annotations
from classes import Customer, Washer, Task, Appointment
from data import (
    customers,
    appointments,
    tasks,
    washers,
    get_next_washer_id,
    get_next_task_id,
)
from utils import (
    find_customer_by_id,
    find_appointment_by_id,
    find_washer_by_id,
    clear_screen,
    pause,
    show_message,
)


def admin_login() -> None:
    clear_screen()
    print("\n=== Admin Login ===")
    password: str = input("Enter admin password: ")

    if password == "admin123":
        print("Welcome, Admin!")
        pause()
        admin_dashboard()
    else:
        show_message("Invalid password!", wait_time=2)


def admin_dashboard() -> None:
    while True:
        clear_screen()
        print("\n=== Admin Dashboard ===")
        print("1. Manage Customers")
        print("2. Manage Appointments")
        print("3. Manage Washers")
        print("4. Assign Tasks")
        print("5. View Reports")
        print("6. Logout")

        choice: str = input("\nEnter your choice: ")

        if choice == "1":
            manage_customers()
        elif choice == "2":
            manage_appointments()
        elif choice == "3":
            manage_washers()
        elif choice == "4":
            assign_tasks()
        elif choice == "5":
            view_reports()
        elif choice == "6":
            print("Logging out...")
            pause()
            break
        else:
            show_message("Invalid choice!", wait_time=1)


def manage_customers() -> None:
    clear_screen()
    print("\n=== Manage Customers ===")
    print("1. View All Customers")
    print("2. Delete Customer")

    choice: str = input("\nEnter your choice: ")

    if choice == "1":
        clear_screen()
        if not customers:
            show_message("No customers found.", wait_time=2)
            return
        print("\n=== All Customers ===")
        for customer in customers:
            print(customer)
        pause()
    elif choice == "2":
        customer_id: int = int(input("Enter customer ID to delete: "))
        customer: Customer | None = find_customer_by_id(customer_id)
        if customer:
            customers.remove(customer)
            show_message("Customer deleted!", wait_time=2)
        else:
            show_message("Customer not found!", wait_time=2)


def manage_appointments() -> None:
    clear_screen()
    print("\n=== Manage Appointments ===")
    print("1. View All Appointments")
    print("2. Cancel Appointment")
    print("3. Mark as Paid")

    choice: str = input("\nEnter your choice: ")

    if choice == "1":
        clear_screen()
        if not appointments:
            show_message("No appointments found.", wait_time=2)
            return
        print("\n=== All Appointments ===")
        for apt in appointments:
            print(apt)
        pause()
    elif choice == "2":
        appointment_id: int = int(input("Enter appointment ID to cancel: "))
        apt: Appointment | None = find_appointment_by_id(appointment_id)
        if apt:
            appointments.remove(apt)
            show_message("Appointment cancelled!", wait_time=2)
        else:
            show_message("Appointment not found!", wait_time=2)
    elif choice == "3":
        appointment_id = int(input("Enter appointment ID: "))
        apt = find_appointment_by_id(appointment_id)
        if apt:
            apt.payment_status = "Paid"
            show_message(f"Appointment {appointment_id} marked as Paid!", wait_time=2)
        else:
            show_message("Appointment not found!", wait_time=2)


def manage_washers() -> None:
    clear_screen()
    print("\n=== Manage Washers ===")
    print("1. View All Washers")
    print("2. Add New Washer")
    print("3. Delete Washer")

    choice: str = input("\nEnter your choice: ")

    if choice == "1":
        clear_screen()
        if not washers:
            show_message("No washers found.", wait_time=2)
            return
        print("\n=== All Washers ===")
        for washer in washers:
            print(washer)
        pause()
    elif choice == "2":
        name: str = input("Enter washer name: ")
        washer_id: int = get_next_washer_id()
        new_washer: Washer = Washer(washer_id, name)
        washers.append(new_washer)
        show_message(f"Washer added! ID: {washer_id}", wait_time=2)
    elif choice == "3":
        washer_id = int(input("Enter washer ID to delete: "))
        washer: Washer | None = find_washer_by_id(washer_id)
        if washer:
            washers.remove(washer)
            show_message("Washer deleted!", wait_time=2)
        else:
            show_message("Washer not found!", wait_time=2)


def assign_tasks() -> None:
    clear_screen()
    print("\n=== Assign Tasks ===")

    print("\nAvailable appointments (without tasks):")
    available_apts: list[Appointment] = [
        apt for apt in appointments if apt.task_id is None
    ]

    if not available_apts:
        show_message("No available appointments.", wait_time=2)
        return

    for apt in available_apts:
        print(
            f"ID: {apt.appointment_id}, Customer: {apt.customer_id}, Date: {apt.date}, Time: {apt.time}, Payment: {apt.payment_method} ({apt.payment_status})"
        )

    appointment_id: int = int(input("\nEnter appointment ID: "))
    apt: Appointment | None = find_appointment_by_id(appointment_id)

    if not apt:
        show_message("Appointment not found!", wait_time=2)
        return

    if apt.task_id is not None:
        show_message("This appointment already has a task!", wait_time=2)
        return

    description: str = input("Enter task description (e.g., Wash, Dry, Iron): ")
    task_id: int = get_next_task_id()
    new_task: Task = Task(task_id, appointment_id, description)
    tasks.append(new_task)
    apt.task_id = task_id

    print("\nAvailable washers:")
    if not washers:
        show_message("No washers available!", wait_time=2)
        return

    for washer in washers:
        print(f"ID: {washer.washer_id}, Name: {washer.name}")

    washer_id: int = int(input("\nEnter washer ID to assign task: "))
    washer = find_washer_by_id(washer_id)

    if washer:
        washer.assigned_tasks.append(task_id)
        apt.status = "In Progress"
        print(f"Task {task_id} assigned to {washer.name}!")
    else:
        print("Washer not found!")


def view_reports() -> None:
    print("\n=== Reports ===")
    print("1. Total Appointments")
    print("2. Completed Tasks")
    print("3. Pending Tasks")
    print("4. Customer Invoice")

    choice: str = input("Enter your choice: ")

    if choice == "1":
        print(f"\nTotal Appointments: {len(appointments)}")
        completed: int = len([apt for apt in appointments if apt.status == "Completed"])
        pending: int = len([apt for apt in appointments if apt.status == "Pending"])
        in_progress: int = len(
            [apt for apt in appointments if apt.status == "In Progress"]
        )
        print(f"Completed: {completed}, Pending: {pending}, In Progress: {in_progress}")

    elif choice == "2":
        completed_tasks: list[Task] = [task for task in tasks if task.status == "Done"]
        if not completed_tasks:
            print("No completed tasks.")
            return
        print("\nCompleted Tasks:")
        for task in completed_tasks:
            print(task)

    elif choice == "3":
        pending_tasks: list[Task] = [task for task in tasks if task.status != "Done"]
        if not pending_tasks:
            print("No pending tasks.")
            return
        print("\nPending Tasks:")
        for task in pending_tasks:
            print(task)

    elif choice == "4":
        customer_id: int = int(input("Enter customer ID: "))
        customer: Customer | None = find_customer_by_id(customer_id)

        if not customer:
            print("Customer not found!")
            return

        print(f"\n=== Invoice for {customer.name} ===")
        print(f"Customer ID: {customer.customer_id}")
        print(f"Email: {customer.email}")

        customer_apts: list[Appointment] = [
            apt for apt in appointments if apt.customer_id == customer_id
        ]

        if not customer_apts:
            print("No appointments found for this customer.")
            return

        print("\nAppointments:")
        total_cost: float = 0
        for apt in customer_apts:
            cost: float = 50
            print(
                f"  - Appointment {apt.appointment_id}: {apt.date} {apt.time} - Status: {apt.status} - Payment: {apt.payment_method} ({apt.payment_status}) - Cost: ${cost}"
            )
            total_cost += cost

        print(f"\nTotal Amount Due: ${total_cost}")
