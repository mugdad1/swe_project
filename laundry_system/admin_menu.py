from __future__ import annotations
import os
import sys
from classes import Customer, Staff, Task, Appointment


def get_password(prompt: str = "Enter your password: ") -> str:
    """Get password - hidden if terminal supports it"""
    print(prompt, end="", flush=True)
    pw = ""
    if os.isatty(sys.stdin.fileno()):
        import termios

        try:
            old = termios.tcgetattr(sys.stdin)
            new = termios.tcgetattr(sys.stdin)
            new[3] = new[3] & ~termios.ECHO
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new)
            pw = sys.stdin.readline().rstrip("\n")
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
            print()
        except:
            pw = sys.stdin.readline().rstrip("\n")
    else:
        pw = sys.stdin.readline().rstrip("\n")
    return pw


from data import (
    customers,
    appointments,
    tasks,
    staff,
    get_next_staff_id,
    get_next_task_id,
    SERVICE_PRICES,
)
from utils import (
    find_customer_by_id,
    find_appointment_by_id,
    find_staff_by_id,
    clear_screen,
    pause,
    show_message,
)


def admin_login() -> None:
    clear_screen()
    print("\n=== Admin Login ===")
    password: str = get_password("Enter admin password: ")

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
        print("3. Manage Staff")
        print("4. Assign Tasks")
        print("5. View Reports")
        print("6. Logout")

        choice: str = input("\nEnter your choice: ")

        if choice == "1":
            manage_customers()
        elif choice == "2":
            manage_appointments()
        elif choice == "3":
            manage_staff()
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
        clear_screen()
        try:
            customer_id: int = int(input("Enter customer ID to delete: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        customer: Customer | None = find_customer_by_id(customer_id)
        if customer:
            customers.remove(customer)
            show_message("Customer deleted!", wait_time=2)
        else:
            show_message("Customer not found!", wait_time=2)
    else:
        show_message("Invalid choice!", wait_time=1)


def manage_appointments() -> None:
    clear_screen()
    print("\n=== Manage Appointments ===")
    print("1. View All Appointments")
    print("2. Cancel Appointment")
    print("3. Mark as Paid")
    print("4. Mark as Completed")

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
        try:
            appointment_id: int = int(input("Enter appointment ID to cancel: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        apt: Appointment | None = find_appointment_by_id(appointment_id)
        if apt:
            appointments.remove(apt)
            show_message("Appointment cancelled!", wait_time=2)
        else:
            show_message("Appointment not found!", wait_time=2)
    elif choice == "3":
        try:
            appointment_id = int(input("Enter appointment ID: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        apt = find_appointment_by_id(appointment_id)
        if apt:
            apt.payment_status = "Paid"
            show_message(f"Appointment {appointment_id} marked as Paid!", wait_time=2)
        else:
            show_message("Appointment not found!", wait_time=2)
    elif choice == "4":
        try:
            appointment_id = int(input("Enter appointment ID: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        apt = find_appointment_by_id(appointment_id)
        if apt:
            apt.status = "Completed"
            show_message(
                f"Appointment {appointment_id} marked as Completed!", wait_time=2
            )
        else:
            show_message("Appointment not found!", wait_time=2)
    else:
        show_message("Invalid choice!", wait_time=1)


def manage_staff() -> None:
    clear_screen()
    print("\n=== Manage Staff ===")
    print("1. View All Staff")
    print("2. Add New Staff")
    print("3. Delete Staff")

    choice: str = input("\nEnter your choice: ")

    if choice == "1":
        clear_screen()
        if not staff:
            show_message("No staff found.", wait_time=2)
            return
        print("\n=== All Staff ===")
        for staff_member in staff:
            print(staff_member)
        pause()
    elif choice == "2":
        clear_screen()
        name: str = input("Enter staff name: ")
        staff_id: int = get_next_staff_id()
        new_staff: Staff = Staff(staff_id, name)
        staff.append(new_staff)
        show_message(f"Staff added! ID: {staff_id}", wait_time=2)
    elif choice == "3":
        clear_screen()
        try:
            staff_id = int(input("Enter staff ID to delete: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        staff_member: Staff | None = find_staff_by_id(staff_id)
        if staff_member:
            staff.remove(staff_member)
            show_message("Staff deleted!", wait_time=2)
        else:
            show_message("Staff not found!", wait_time=2)
    else:
        show_message("Invalid choice!", wait_time=1)


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
        items = (
            f"{apt.item_count} {apt.item_types}"
            if apt.item_types
            else f"{apt.item_count} pcs"
        )
        print(
            f"ID: {apt.appointment_id}, Customer: {apt.customer_id}, "
            f"Service: {apt.service_type}, Items: {items}, "
            f"Date: {apt.date}, Payment: {apt.payment_method} ({apt.payment_status})"
        )

    try:
        appointment_id: int = int(input("\nEnter appointment ID: "))
    except ValueError:
        show_message("Invalid ID! Enter a number.", wait_time=2)
        return
    apt: Appointment | None = find_appointment_by_id(appointment_id)

    if not apt:
        show_message("Appointment not found!", wait_time=2)
        return

    if apt.task_id is not None:
        show_message("This appointment already has a task!", wait_time=2)
        return

    description: str = apt.service_type
    print(f"Task Description: {description}")
    task_id: int = get_next_task_id()
    new_task: Task = Task(task_id, appointment_id, description)
    tasks.append(new_task)
    apt.task_id = task_id

    print("\nAvailable staff:")
    if not staff:
        show_message("No staff available!", wait_time=2)
        return

    for staff_member in staff:
        print(f"ID: {staff_member.staff_id}, Name: {staff_member.name}")

    try:
        staff_id: int = int(input("\nEnter staff ID to assign task: "))
    except ValueError:
        show_message("Invalid ID! Enter a number.", wait_time=2)
        return
    staff_member = find_staff_by_id(staff_id)

    if staff_member:
        staff_member.assigned_tasks.append(task_id)
        apt.status = "In Progress"
        print(f"Task {task_id} assigned to {staff_member.name}!")
    else:
        print("Staff not found!")


def view_reports() -> None:
    clear_screen()
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
        pause()

    elif choice == "2":
        completed_tasks: list[Task] = [task for task in tasks if task.status == "Done"]
        if not completed_tasks:
            print("No completed tasks.")
            pause()
            return
        print("\nCompleted Tasks:")
        for task in completed_tasks:
            print(task)
        pause()

    elif choice == "3":
        pending_tasks: list[Task] = [task for task in tasks if task.status != "Done"]
        if not pending_tasks:
            print("No pending tasks.")
            pause()
            return
        print("\nPending Tasks:")
        for task in pending_tasks:
            print(task)
        pause()

    elif choice == "4":
        try:
            customer_id: int = int(input("Enter customer ID: "))
        except ValueError:
            show_message("Invalid ID! Enter a number.", wait_time=2)
            return
        customer: Customer | None = find_customer_by_id(customer_id)

        if not customer:
            print("Customer not found!")
            pause()
            return

        print(f"\n=== Invoice for {customer.name} ===")
        print(f"Customer ID: {customer.customer_id}")
        print(f"Email: {customer.email}")

        customer_apts: list[Appointment] = [
            apt for apt in appointments if apt.customer_id == customer_id
        ]

        if not customer_apts:
            print("No appointments found for this customer.")
            pause()
            return

        print("\nAppointments:")
        total_cost: float = 0
        for apt in customer_apts:
            base_price = SERVICE_PRICES.get(apt.service_type, 15)
            cost = base_price * max(apt.item_count, 1)
            items = (
                f"{apt.item_count} {apt.item_types}"
                if apt.item_types
                else f"{apt.item_count} pcs"
            )
            print(
                f"  - Appointment {apt.appointment_id}: {apt.date} {apt.time} "
                f"Service: {apt.service_type}, Items: {items}, "
                f"Status: {apt.status}, Payment: {apt.payment_method} ({apt.payment_status}), "
                f"Cost: {cost} SR"
            )
            total_cost += cost

        print(f"\nTotal Amount Due: {total_cost} SR")
        pause()
