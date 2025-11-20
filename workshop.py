from datetime import datetime

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
        return (f"Customer: {self.customer.username}, Date: {self.date}, "
                f"Time: {self.time}, Status: {self.status}, Mechanic: {mech_name}, "
                f"Comments: {self.comments}")

# In-memory storage
users = []
jobs = []

# Create default admin and mechanic
users.append(Admin("admin", "admin"))
users.append(Mechanic("mech1", "mech1"))

def find_user(username):
    for u in users:
        if u.username == username:
            return u
    return None

def login(role):
    username = input("Username: ")
    password = input("Password: ")
    user = find_user(username)
    if user and user.password == password and user.role == role:
        print(f"Logged in as {role} '{username}'")
        return user
    print("Login failed")
    return None

def is_valid_date(date_str):
    """Check if the date string is valid format YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    """Check if the time string is valid format HH:MM."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def register_customer():
    username = input("Choose customer username: ")
    if find_user(username):
        print("Username already exists")
        return
    password = input("Choose password: ")
    customer = Customer(username, password)
    users.append(customer)
    print("Customer registered:", username)
def customer_actions(customer):
    # assume `jobs` is a global list that stores all ServiceJob objects
    global jobs

    while True:
        print("\nCustomer Menu: 1-Book Service, 2-View My Jobs, 3-Logout")
        choice = input("Select: ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ").strip()
            if not is_valid_date(date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            time = input("Time (HH:MM): ").strip()
            # ---- corrected indentation ----
            if not is_valid_time(time):
                print("Invalid time format. Please use HH:MM.")
                continue

            # optional: prevent duplicate bookings
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

        else:
            print("Invalid choice")

# -------------------------------------------------
# Customer account‑management helpers
# -------------------------------------------------
def view_account(customer: Customer):
    """Display basic account information."""
    print("\n--- Account Details ---")
    print(f"Username : {customer.username}")
    print(f"Role     : {customer.role}")
    print("-----------------------\n")


def change_password(customer: Customer):
    """Allow the customer to change their password."""
    current = input("Enter current password: ")
    if current != customer.password:
        print("Incorrect password – aborting.")
        return

    new_pw = input("Enter new password: ")
    confirm = input("Confirm new password: ")
    if new_pw != confirm:
        print("Passwords do not match – aborting.")
        return

    if not new_pw:
        print("Password cannot be empty.")
        return

    customer.password = new_pw
    print("Password updated successfully.")


# -------------------------------------------------
# Updated customer menu – now includes account mgmt
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
            # ---- booking (unchanged) ----
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
            # ---- view jobs (unchanged) ----
            print("My Jobs:")
            for j in customer.jobs:
                print(" -", j.summary())

        elif choice == "3":
            break

        elif choice == "4":
            # ---- manage account ----
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



def mechanic_actions(mechanic):
    while True:
        print("\nMechanic Menu: 1-View My Jobs, 2-Update Job, 3-Logout")
        choice = input("Select: ")
        if choice == "1":
            print("Assigned Jobs:")
            for j in mechanic.assigned_jobs:
                print(" -", j.summary())
        elif choice == "2":
            if not mechanic.assigned_jobs:
                print("No jobs assigned")
                continue
            for i, j in enumerate(mechanic.assigned_jobs):
                print(f"{i + 1}. {j.summary()}")
            sel = int(input("Select job number: ")) - 1
            if 0 <= sel < len(mechanic.assigned_jobs):
                job = mechanic.assigned_jobs[sel]
                status = input("New status (Pending / In Progress / Completed): ")
                if status not in ["Pending", "In Progress", "Completed"]:
                    print("Invalid status. Please use Pending, In Progress, or Completed.")
                    continue
                job.status = status
                comments = input("Comments: ")
                job.comments = comments
                print("Job updated:", job.summary())
            else:
                print("Invalid number")
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def assign_job_logic():
    """Assign an unassigned pending job to a mechanic."""
    # Find jobs that are still pending and have no mechanic
    pending_jobs = [j for j in jobs if j.status == "Pending" and j.mechanic is None]

    if not pending_jobs:
        print("No pending jobs to assign.")
        return

    # List pending jobs
    print("\nPending Jobs:")
    for idx, job in enumerate(pending_jobs, start=1):
        print(f"{idx}. {job.summary()}")

    # Choose a job
    try:
        job_idx = int(input("Select job number to assign: ")) - 1
        job = pending_jobs[job_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # List available mechanics
    mechanics = [u for u in users if isinstance(u, Mechanic)]
    if not mechanics:
        print("No mechanics available.")
        return

    print("\nMechanics:")
    for idx, mech in enumerate(mechanics, start=1):
        print(f"{idx}. {mech.username}")

    # Choose a mechanic
    try:
        mech_idx = int(input("Select mechanic number: ")) - 1
        mechanic = mechanics[mech_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Perform assignment
    job.mechanic = mechanic
    mechanic.assigned_jobs.append(job)
    print(f"Job assigned to {mechanic.username}:")
    print(job.summary())

def generate_report_logic():
    """Print a quick status report for all service jobs."""
    total = len(jobs)
    pending   = sum(1 for j in jobs if j.status == "Pending")
    in_prog   = sum(1 for j in jobs if j.status == "In Progress")
    completed = sum(1 for j in jobs if j.status == "Completed")

    print("\n--- Service Job Report ---")
    print(f"Total jobs      : {total}")
    print(f"Pending         : {pending}")
    print(f"In Progress     : {in_prog}")
    print(f"Completed       : {completed}")

    # Jobs per mechanic
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
    """Display all registered customers and their jobs."""
    customers = [u for u in users if isinstance(u, Customer)]

    if not customers:
        print("\nNo customers registered.\n")
        return

    print("\n--- Customer Records ---")
    for cust in customers:
        print(f"\nUsername : {cust.username}")
        print(f"Role     : {cust.role}")
        print(f"Jobs     : {len(cust.jobs)}")
        if cust.jobs:
            for idx, job in enumerate(cust.jobs, start=1):
                print(f"  {idx}. {job.summary()}")
    print("------------------------\n")


def delete_customer():
    """Remove a customer and all of their associated jobs."""
    customers = [u for u in users if isinstance(u, Customer)]

    if not customers:
        print("\nNo customers to delete.\n")
        return

    # List customers with an index
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

    # Remove the customer's jobs from the global job list
    global jobs
    jobs = [j for j in jobs if j.customer != customer]

    # Also remove any of those jobs from mechanics' assigned lists
    for mech in (u for u in users if isinstance(u, Mechanic)):
        mech.assigned_jobs = [j for j in mech.assigned_jobs if j.customer != customer]

    # Finally remove the customer object from the users list
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
            assign_job_logic()          # <-- real implementation
        elif choice == "2":
            generate_report_logic()     # keep your existing code
        elif choice == "3":
            break
        elif choice == "4":
            view_customer_detail()
        elif choice == "5":
            delete_customer()
        else:
            print("Invalid choice")

def main():
    while True:
        print("\nMain Menu: 1-Register Customer, 2-Login Customer, 3-Login Mechanic, 4-Login Admin, 5-Exit")
        choice = input("Select: ")
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