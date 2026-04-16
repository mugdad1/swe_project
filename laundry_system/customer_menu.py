from __future__ import annotations
from classes import Customer, Appointment
from data import (
    customers,
    appointments,
    get_next_customer_id,
    get_next_appointment_id,
    PAYMENT_METHODS,
    FAKE_PAYMENT_DETAILS,
    SERVICE_TYPES,
)
from utils import (
    find_customer_by_email,
    get_customer_appointments,
    find_task_by_id,
    clear_screen,
    pause,
    show_message,
    validate_email,
    validate_date,
    validate_time,
)


def customer_signup() -> None:
    clear_screen()
    print("\n=== Customer Sign Up ===")
    name: str = input("Enter your name: ")
    email: str = input("Enter your email: ")

    if not validate_email(email):
        show_message("Invalid email format!", wait_time=2)
        return

    if find_customer_by_email(email):
        show_message("Email already registered!", wait_time=2)
        return

    password: str = input("Enter your password: ")

    customer_id: int = get_next_customer_id()
    new_customer: Customer = Customer(customer_id, name, email, password)
    customers.append(new_customer)

    show_message(f"Sign up successful! Your ID is: {customer_id}", wait_time=3)


def customer_login() -> None:
    clear_screen()
    print("\n=== Customer Login ===")
    email: str = input("Enter your email: ")
    password: str = input("Enter your password: ")

    customer: Customer | None = find_customer_by_email(email)

    if customer and customer.password == password:
        print(f"Welcome, {customer.name}!")
        pause()
        customer_dashboard(customer)
    else:
        show_message("Invalid email or password!", wait_time=2)


def customer_dashboard(customer: Customer) -> None:
    while True:
        clear_screen()
        print(f"\n=== Customer Dashboard ({customer.name}) ===")
        print("1. Book a Service")
        print("2. View My Appointments")
        print("3. View Appointment Details")
        print("4. Cancel Appointment")
        print("5. Logout")

        choice: str = input("\nEnter your choice: ")

        if choice == "1":
            book_service(customer)
        elif choice == "2":
            view_appointments(customer)
        elif choice == "3":
            view_appointment_details(customer)
        elif choice == "4":
            cancel_appointment(customer)
        elif choice == "5":
            print("Logging out...")
            pause()
            break
        else:
            show_message("Invalid choice!", wait_time=1)


def book_service(customer: Customer) -> None:
    clear_screen()
    print("\n=== Book a Service ===")
    date: str = input("Enter date (YYYY-MM-DD): ")
    while not validate_date(date):
        print("Invalid date format! Use YYYY-MM-DD (e.g., 2024-04-20)")
        date = input("Enter date (YYYY-MM-DD): ")

    time: str = input("Enter time (HH:MM): ")
    while not validate_time(time):
        print("Invalid time format! Use HH:MM (e.g., 10:00)")
        time = input("Enter time (HH:MM): ")

    print("\n=== Select Service ===")
    print("1. Wash")
    print("2. Dry Clean")
    print("3. Iron")
    print("4. Wash & Iron")
    print("5. Express Service")
    print("6. Other (custom)")

    service_choice: str = input("\nEnter your choice (1-6): ")

    if service_choice not in ["1", "2", "3", "4", "5", "6"]:
        show_message("Invalid choice! Defaulting to Wash.", wait_time=2)
        service_choice = "1"

    service_type: str = SERVICE_TYPES[service_choice]

    if service_type == "Other":
        service_type = input("Enter custom service description: ")

    item_count: int = 0
    while item_count <= 0:
        try:
            item_count = int(input("\nHow many pieces? "))
            if item_count <= 0:
                print("Please enter a valid number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    item_types: str = input("Enter item types (e.g., T-shirts, Pants, Dresses): ")

    print("\n=== Choose Payment Method ===")
    print("1. Cash (on delivery)")
    print("2. Credit Card")
    print("3. IBAN Transfer")
    print("4. STC Pay")

    payment_choice: str = input("\nEnter your choice (1-4): ")

    if payment_choice not in ["1", "2", "3", "4"]:
        show_message("Invalid choice! Defaulting to Cash.", wait_time=2)
        payment_choice = "1"

    payment_method: str = PAYMENT_METHODS[payment_choice]

    if payment_method == "IBAN Transfer":
        print("\n" + "=" * 35)
        print("--- IBAN Transfer ---")
        print(f"Account Holder: {FAKE_PAYMENT_DETAILS['iban_holder']}")
        print(f"Bank: {FAKE_PAYMENT_DETAILS['iban_bank']}")
        print(f"IBAN: {FAKE_PAYMENT_DETAILS['iban']}")
        print("=" * 35)
        input("\nPress Enter to continue...")
    elif payment_method == "STC Pay":
        print("\n" + "=" * 30)
        print("--- STC Pay ---")
        print(f"Send to: {FAKE_PAYMENT_DETAILS['stc_pay']}")
        print("=" * 30)
        input("\nPress Enter to continue...")

    appointment_id: int = get_next_appointment_id()
    new_appointment: Appointment = Appointment(
        appointment_id,
        customer.customer_id,
        date,
        time,
        payment_method=payment_method,
        payment_status="Pending",
        service_type=service_type,
        item_count=item_count,
        item_types=item_types,
    )
    appointments.append(new_appointment)
    customer.appointments.append(appointment_id)

    show_message(
        f"Appointment booked! Your appointment ID is: {appointment_id}", wait_time=3
    )


def view_appointments(customer: Customer) -> None:
    clear_screen()
    print("\n=== Your Appointments ===")
    customer_appointments: list[Appointment] = get_customer_appointments(
        customer.customer_id
    )

    if not customer_appointments:
        show_message("You have no appointments.", wait_time=2)
        return

    for apt in customer_appointments:
        print(apt)

    pause()


def view_appointment_details(customer: Customer) -> None:
    clear_screen()
    print("\n=== View Appointment Details ===")
    appointment_id: int = int(input("Enter appointment ID: "))

    apt: Appointment | None = None
    for appointment in appointments:
        if (
            appointment.appointment_id == appointment_id
            and appointment.customer_id == customer.customer_id
        ):
            apt = appointment
            break

    if apt:
        print(f"\nAppointment ID: {apt.appointment_id}")
        print(f"Date: {apt.date}")
        print(f"Time: {apt.time}")
        print(f"Status: {apt.status}")
        print(f"Service: {apt.service_type}")
        print(f"Items: {apt.item_count} pieces - {apt.item_types}")
        if apt.task_id:
            task = find_task_by_id(apt.task_id)
            if task:
                print(f"Task ID: {apt.task_id}")
                print(f"  Description: {task.description}")
                print(f"  Status: {task.status}")
                if task.notes:
                    print(f"  Notes: {task.notes}")
        print(f"Payment Method: {apt.payment_method}")
        print(f"Payment Status: {apt.payment_status}")
    else:
        show_message("Appointment not found!", wait_time=2)
        return

    pause()


def cancel_appointment(customer: Customer) -> None:
    clear_screen()
    print("\n=== Cancel Appointment ===")
    appointment_id: int = int(input("Enter appointment ID: "))

    apt: Appointment | None = None
    for appointment in appointments:
        if (
            appointment.appointment_id == appointment_id
            and appointment.customer_id == customer.customer_id
        ):
            apt = appointment
            break

    if apt:
        if apt.status == "Completed":
            show_message("Cannot cancel completed appointment!", wait_time=2)
            return
        appointments.remove(apt)
        customer.appointments.remove(appointment_id)
        show_message("Appointment cancelled!", wait_time=2)
    else:
        show_message("Appointment not found!", wait_time=2)
