# service_center.py
from datetime import datetime
import getpass

# -------------------------------------------------
# User classes
# -------------------------------------------------
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "customer")
        self.jobs = []


class Mechanic(User):
    def __init__(self, username, password):
        super().__init__(username, password, "mechanic")
        self.assigned_jobs = []


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")


# -------------------------------------------------
# Service job model
# -------------------------------------------------
class ServiceJob:
    def __init__(self, customer, date, time):
        self.customer = customer
        self.date = date
        self.time = time
        self.status = "Pending"
        self.comments = ""
        self.mechanic = None

    def summary(self):
        mech_name = self.mechanic.username if self.mechanic else "None"
        return (
            f"Customer: {self.customer.username}, Date: {self.date}, "
            f"Time: {self.time}, Status: {self.status}, Mechanic: {mech_name}, "
            f"Comments: {self.comments}"
        )


# -------------------------------------------------
# In‑memory storage
# -------------------------------------------------
users = []
jobs = []

# default admin & mechanic
users.append(Admin("admin", "admin"))
users.append(Mechanic("mech1", "mech1"))


def find_user(username):
    for u in users:
        if u.username == username:
            return u
    return None


def login(role):
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    user = find_user(username)

    if not user:
        print("Login failed – unknown user")
        return None
    if user.password != password:
        print("Login failed – incorrect password")
        return None
    if user.role != role:
        print(f"Login failed – user is not a {role}")
        return None

    print(f"Logged in as {role} '{username}'")
    return user


# -------------------------------------------------
# Validation helpers
# -------------------------------------------------
def is_valid_date(date_str):
    """YYYY‑MM‑DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_time(time_str):
    """HH:MM  (00‑23 for hour)"""
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.hour < 24
    except ValueError:
        return False


# -------------------------------------------------
# Customer helpers
# -------------------------------------------------
def view_account(customer: Customer):
    print("\n--- Account Details ---")
    print(f"Username : {customer.username}")
    print(f"Role     : {customer.role}")
    print("-----------------------\n")


def change_password(customer: Customer):
    current = getpass.getpass("Enter current password: ")
    if current != customer.password:
        print("Incorrect password – aborting.")
        return

    new_pw = getpass.getpass("Enter new password: ")
    confirm = getpass.getpass("Confirm new password: ")
    if new_pw != confirm:
        print("Passwords do not match – aborting.")
        return
    if not new_pw.strip():
        print("Password cannot be empty.")
        return

    customer.password = new_pw
    print("Password updated successfully.")


def register_customer():
    username = input("Choose customer username: ")
    if find_user(username):
        print("Username already exists")
        return
    password = getpass.getpass("Choose password: ")
    if not password.strip():
        print("Password cannot be empty.")
        return
    customer = Customer(username, password)
    users.append(customer)
    print("Customer registered:", username)


# -------------------------------------------------
# Customer menu (includes account management)
# -------------------------------------------------
def customer_actions(customer: Customer):
    global jobs
    while True:
        print(
            "\nCustomer Menu: "
            "1‑Book Service, 2‑View My Jobs, 3‑Logout, 4‑Manage Account"
        )
        choice = input("Select: ").strip()

        if choice == "1":
            date = input("Date (YYYY‑MM‑DD): ").strip()
            if not is_valid_date(date):
                print("Invalid date format. Please use YYYY‑MM‑DD.")
                continue

            time = input("Time (HH:MM): ").strip()
            if not is_valid_time(time):
                print("Invalid time format. Please use HH:MM.")
                continue

            if any(j.date == date and j.time == time for j in customer.jobs):
                print("You already have a booking at that date and time.")
                continue

            job = ServiceJob(customer, date, time)
            jobs.append(job)
            customer.jobs.append(job)
            print("Service booked:", job.summary())

        elif choice == "2":
            print("My Jobs:")
            for j in customer.jobs:
                print(" -", j.summary())

        elif choice == "3":
            break

        elif choice == "4":
            while True:
                print(
                    "\nAccount Menu: 1‑View Details, 2‑Change Password, 3‑Back"
                )
                sub = input("Select: ").strip()
                if sub == "1":
                    view_account(customer)
                elif sub == "2":
                    change_password(customer)
                elif sub == "3":
                    break
                else:
                    print("Invalid choice")
        else:
            print("Invalid choice")


# -------------------------------------------------
# Mechanic menu
# -------------------------------------------------
def mechanic_actions(mechanic: Mechanic):
    while True:
        print("\nMechanic Menu: 1‑View My Jobs, 2‑Update Job, 3‑Logout")
        choice = input("Select: ").strip()
        if choice == "1":
            print("Assigned Jobs:")
            for j in mechanic.assigned_jobs:
                print(" -", j.summary())

        elif choice == "2":
            if not mechanic.assigned_jobs:
                print("No jobs assigned")
                continue
            for i, j in enumerate(mechanic.assigned_jobs, start=1):
                print(f"{i}. {j.summary()}")
            try:
                sel = int(input("Select job number: ")) - 1
                job = mechanic.assigned_jobs[sel]
            except (ValueError, IndexError):
                print("Invalid selection.")
                continue

            status = input("New status (Pending / In Progress / Completed): ").title()
            if status not in ["Pending", "In Progress", "Completed"]:
                print("Invalid status. Use Pending, In Progress, or Completed.")
                continue
            job.status = status
            job.comments = input("Comments: ")
            print("Job updated:", job.summary())

        elif choice == "3":
            break
        else:
            print("Invalid choice")


# -------------------------------------------------
# Admin helpers
# -------------------------------------------------
def assign_job_logic():
    """Assign a pending, un‑assigned job to a mechanic."""
    pending_jobs = [j for j in jobs if j.status == "Pending" and j.mechanic is None]
    if not pending_jobs:
        print("No pending jobs to assign.")
        return

    print("\nPending Jobs:")
    for idx, job in enumerate(pending_jobs, start=1):
        print(f"{idx}. {job.summary()}")

    try:
        job_idx = int(input("Select job number to assign: ")) - 1
        job = pending_jobs[job_idx]
    except (ValueError, IndexError):
        print("Please enter a valid job number.")
        return

    mechanics = [u for u in users if isinstance(u, Mechanic)]
    if not mechanics:
        print("No mechanics available.")
        return

    print("\nMechanics:")
    for idx, mech in enumerate(mechanics, start=1):
        print(f"{idx}. {mech.username}")

    try:
        mech_idx = int(input("Select mechanic number: ")) - 1
        mechanic = mechanics[mech_idx]
    except (ValueError, IndexError):
        print("Please enter a valid mechanic number.")
        return

    # perform assignment
    job.mechanic = mechanic
    mechanic.assigned_jobs.append(job)
    job.status = "In Progress"          # prevents double‑assignment
    print(f"Job assigned to {mechanic.username}:")
    print(job.summary())


def generate_report_logic():
    total = len(jobs)
    pending = sum(1 for j in jobs if j.status == "Pending")
    in_progress = sum(1 for j in jobs if j.status == "In Progress")
    completed = sum(1 for j in jobs if j.status == "Completed")

    print("\n--- Service Job Report ---")
    print(f"Total jobs      : {total}")
    print(f"Pending         : {pending}")
    print(f"In Progress     : {in_progress}")
    print(f"Completed       : {completed}")

    mechanics = [u for u in users if isinstance(u, Mechanic)]
    if mechanics:
        print("\nJobs assigned to mechanics:")
        for mech in mechanics:
            count = len(mech.assigned_jobs)
            print(f"  {mech.username}: {count} job{'s' if count != 1 else ''}")
    else:
        print("\nNo mechanics in the system.")
    print("---------------------------\n")


def view_customer_detail():
    """Show all customers and their jobs."""
    customers = [u for u in users if isinstance(u, Customer)]
    if not customers:
        print("\nNo customers registered.\n")
        return

    print("\n--- Customer Records ---")
    for cust in customers:
        print(f"\nUsername : {cust.username}")
        print(f"Role     : {cust.role}")
        print(f"Jobs     : {len(cust.jobs)}")
        for idx, job in enumerate(cust.jobs, start=1):
            print(f"  {idx}. {job.summary()}")
    print("------------------------\n")


def delete_customer():
    """Remove a customer and all of their jobs."""
    customers = [u for u in users if isinstance(u, Customer)]
    if not customers:
        print("\nNo customers to delete.\n")
        return

    print("\nCustomers:")
    for idx, cust in enumerate(customers, start=1):
        print(f"{idx}. {cust.username}")

    try:
        sel = int(input("Select customer number to delete: ")) - 1
        customer = customers[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    confirm = input(
        f"Are you sure you want to delete '{customer.username}' and all their jobs? (yes/no): "
    ).strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    # Remove the customer's jobs from the global list (in‑place)
    global jobs
    jobs[:] = [j for j in jobs if j.customer != customer]

    # Remove those jobs from any mechanic's assigned list
    for mech in (u for u in users if isinstance(u, Mechanic)):
        mech.assigned_jobs[:] = [j for j in mech.assigned_jobs if j.customer != customer]

    # Finally remove the customer object
    users.remove(customer)

    print(f"Customer '{customer.username}' and all related jobs have been deleted.\n")


def admin_actions(admin: Admin):
    while True:
        print(
            "\nAdmin Menu: "
            "1‑Assign Job, 2‑Generate Report, 3‑Logout, "
            "4‑View Customer Records, 5‑Delete Customer"
        )
        choice = input("Select: ").strip()

        if choice == "1":
            assign_job_logic()
        elif choice == "2":
            generate_report_logic()
        elif choice == "3":
            break
        elif choice == "4":
            view_customer_detail()
        elif choice == "5":
            delete_customer()
        else:
            print("Invalid choice")


# -------------------------------------------------
# Main loop
# -------------------------------------------------
def main():
    while True:
        print(
            "\nMain Menu: 1‑Register Customer, 2‑Login Customer, "
            "3‑Login Mechanic, 4‑Login Admin, 5‑Exit"
        )
        choice = input("Select: ").strip()
        if choice == "1":
            register_customer()
        elif choice == "2":
            user = login("customer")
            if user:
                customer_actions(user)
        elif choice == "3":
            user = login("mechanic")
            if user:
                mechanic_actions(user)
        elif choice == "4":
            user = login("admin")
            if user:
                admin_actions(user)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
