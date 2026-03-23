from classes import Customer, Appointment
from data import customers, appointments, get_next_customer_id, get_next_appointment_id
from utils import find_customer_by_email, find_customer_by_id, get_customer_appointments, clear_screen, pause, show_message


def customer_signup():
    """Register a new customer"""
    clear_screen()
    print("\n=== Customer Sign Up ===")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Check if email already exists
    if find_customer_by_email(email):
        show_message("Email already registered!", wait_time=2)
        return

    # Create new customer
    customer_id = get_next_customer_id()
    new_customer = Customer(customer_id, name, email, password)
    customers.append(new_customer)

    show_message(f"Sign up successful! Your ID is: {customer_id}", wait_time=3)


def customer_login():
    """Login as a customer"""
    clear_screen()
    print("\n=== Customer Login ===")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Find customer
    customer = find_customer_by_email(email)

    if customer and customer.password == password:
        print(f"Welcome, {customer.name}!")
        pause()
        customer_dashboard(customer)
    else:
        show_message("Invalid email or password!", wait_time=2)


def customer_dashboard(customer):
    """Customer main menu"""
    while True:
        clear_screen()
        print(f"\n=== Customer Dashboard ({customer.name}) ===")
        print("1. Book a Service")
        print("2. View My Appointments")
        print("3. View Appointment Details")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            book_service(customer)
        elif choice == "2":
            view_appointments(customer)
        elif choice == "3":
            view_appointment_details(customer)
        elif choice == "4":
            print("Logging out...")
            pause()
            break
        else:
            show_message("Invalid choice!", wait_time=1)


def book_service(customer):
    """Book a laundry service appointment"""
    clear_screen()
    print("\n=== Book a Service ===")
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")

    # Create appointment
    appointment_id = get_next_appointment_id()
    new_appointment = Appointment(appointment_id, customer.customer_id, date, time)
    appointments.append(new_appointment)
    customer.appointments.append(appointment_id)

    show_message(f"Appointment booked! Your appointment ID is: {appointment_id}", wait_time=3)


def view_appointments(customer):
    """View all appointments for the customer"""
    clear_screen()
    print("\n=== Your Appointments ===")
    customer_appointments = get_customer_appointments(customer.customer_id)

    if not customer_appointments:
        show_message("You have no appointments.", wait_time=2)
        return

    for apt in customer_appointments:
        print(apt)

    pause()


def view_appointment_details(customer):
    """View details of a specific appointment"""
    clear_screen()
    print("\n=== View Appointment Details ===")
    appointment_id = int(input("Enter appointment ID: "))

    apt = None
    for appointment in appointments:
        if appointment.appointment_id == appointment_id and appointment.customer_id == customer.customer_id:
            apt = appointment
            break

    if apt:
        print(f"\nAppointment ID: {apt.appointment_id}")
        print(f"Date: {apt.date}")
        print(f"Time: {apt.time}")
        print(f"Status: {apt.status}")
        if apt.task_id:
            print(f"Task ID: {apt.task_id}")
    else:
        show_message("Appointment not found!", wait_time=2)
        return

    pause()
