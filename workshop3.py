from datetime import datetime
import getpass
import sys

# --- Utilities ---

def secure_input(prompt):
    """Use getpass if terminal, else fallback to input."""
    if sys.stdin.isatty():
        try:
            return getpass.getpass(prompt)
        except Exception:
            print("Warning: falling back to standard input for password.")
            return input(prompt)
    else:
        return input(prompt)

def is_valid_date(date_str):
    """Validate YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    """Validate HH:MM format (00:00–23:59)."""
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        return 0 <= dt.hour < 24
    except ValueError:
        return False

def find_user(username):
    return next((u for u in users if u.username == username), None)

# --- Models / Data Classes ---

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
        mech = self.mechanic.username if self.mechanic else "None"
        return (f"Customer: {self.customer.username}, Date: {self.date}, "
                f"Time: {self.time}, Status: {self.status}, Mechanic: {mech}, "
                f"Comments: {self.comments}")

class Invoice:
    def __init__(self, job):
        self.job = job
        self.feedback = None

# --- In-memory Storage ---

users = []
jobs = []

# Default admin + some sample mechanics
users.append(Admin("admin", "admin"))
users.append(Mechanic("mech1", "mech1"))
users.append(Mechanic("mech2", "mech2"))

# --- Authentication / Login ---

def login(role):
    username = input("Username: ")
    password = secure_input("Password: ")
    user = find_user(username)
    if not user:
        print("Login failed – unknown user.")
        return None
    if user.password != password:
        print("Login failed – incorrect password.")
        return None
    if user.role != role:
        print(f"Login failed – user is not a {role}.")
        return None
    print(f"Logged in as {role} '{username}'.")
    return user

# --- Customer registration & account management ---

def register_customer():
    username = input("Choose customer username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if find_user(username):
        print("Username already exists.")
        return
    password = secure_input("Choose password: ")
    if not password.strip():
        print("Password cannot be empty.")
        return
    users.append(Customer(username, password))
    print("Customer registered:", username)

def view_account(customer):
    print("\n--- Account Details ---")
    print(f"Username: {customer.username}")
    print(f"Role    : {customer.role}")
    print("------------------------\n")

def change_password(customer):
    current = secure_input("Enter current password: ")
    if current != customer.password:
        print("Incorrect password.")
        return
    new_pw = secure_input("New password: ")
    confirm = secure_input("Confirm new password: ")
    if new_pw != confirm:
        print("Passwords do not match.")
        return
    if not new_pw.strip():
        print("Password cannot be empty.")
        return
    customer.password = new_pw
    print("Password updated successfully.")

def delete_own_account(customer):
    pw = secure_input("Enter your password to confirm deletion: ")
    if pw != customer.password:
        print("Incorrect password. Deletion cancelled.")
        return False
    confirm = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return False
    # Remove customer jobs
    global jobs
    jobs = [job for job in jobs if job.customer != customer]
    # Remove user
    users.remove(customer)
    print("Account deleted.")
    return True

# --- Customer menu / actions ---

def _customer_book_service(customer):
    date = input("Date (YYYY-MM-DD): ").strip()
    if not is_valid_date(date):
        print("Invalid date format.")
        return
    time = input("Time (HH:MM): ").strip()
    if not is_valid_time(time):
        print("Invalid time format.")
        return
    if any(j.date == date and j.time == time for j in customer.jobs):
        print("You already have a booking at that date/time.")
        return
    job = ServiceJob(customer, date, time)
    jobs.append(job)
    customer.jobs.append(job)
    print("Service booked:", job.summary())

def _customer_view_jobs(customer):
    if not customer.jobs:
        print("No jobs yet.")
        return
    print("My Jobs:")
    for j in customer.jobs:
        print(" -", j.summary())

def _customer_manage_account(customer):
    sub_menu = {
        "1": ("View Details", view_account),
        "2": ("Change Password", change_password),
        "3": ("Delete Account", delete_own_account),
        "4": ("Back", None),
    }
    while True:
        print("\n--- Account Menu ---")
        for key, (desc, _) in sub_menu.items():
            print(f"{key}. {desc}")
        choice = input("Select: ").strip()
        if choice == "4":
            break
        action = sub_menu.get(choice)
        if action:
            func = action[1]
            if func:
                result = func(customer)
                if choice == "3" and result:
                    return  # account deleted → exit
        else:
            print("Invalid choice, try again.")

def _customer_add_feedback(customer):
    completed = [job for job in customer.jobs if job.status == "Completed"]
    if not completed:
        print("No completed jobs to add feedback to.")
        return
    for i, job in enumerate(completed, start=1):
        print(f"{i}. {job.summary()}")
    try:
        sel = int(input("Select job to add feedback: ")) - 1
        job = completed[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    if not hasattr(job, "invoice"):
        print("No invoice for that job.")
        return
    feedback = input("Enter feedback: ").strip()
    job.invoice.feedback = feedback
    print("Feedback added successfully.")

def customer_actions(customer: Customer):
    menu = {
        "1": ("Book Service", _customer_book_service),
        "2": ("My Jobs", _customer_view_jobs),
        "3": ("Manage Account", _customer_manage_account),
        "4": ("Add Feedback", _customer_add_feedback),
        "5": ("Logout", None),
    }
    while True:
        print("\n--- Customer Menu ---")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
        choice = input("Select: ").strip()
        if choice == "5":
            break
        action = menu.get(choice)
        if action:
            func = action[1]
            if func:
                func(customer)
        else:
            print("Invalid choice, try again.")

# --- Mechanic menu / actions ---

def _mechanic_view_jobs(mechanic: Mechanic):
    if not mechanic.assigned_jobs:
        print("No assigned jobs.")
        return
    print("Assigned Jobs:")
    for j in mechanic.assigned_jobs:
        print(" -", j.summary())

def _mechanic_update_job(mechanic: Mechanic):
    if not mechanic.assigned_jobs:
        print("No jobs assigned.")
        return
    for i, j in enumerate(mechanic.assigned_jobs, start=1):
        print(f"{i}. {j.summary()}")
    try:
        sel = int(input("Select job number: ")) - 1
        job = mechanic.assigned_jobs[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    new_status = input("New status (Pending / In Progress / Completed): ").title()
    if new_status not in {"Pending", "In Progress", "Completed"}:
        print("Invalid status.")
        return
    job.status = new_status
    job.comments = input("Comments (optional): ").strip()
    print("Job updated:", job.summary())

def mechanic_actions(mechanic: Mechanic):
    menu = {
        "1": ("View My Jobs", _mechanic_view_jobs),
        "2": ("Update Job Status", _mechanic_update_job),
        "3": ("Logout", None),
    }
    while True:
        print("\n--- Mechanic Menu ---")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
        choice = input("Select: ").strip()
        if choice == "3":
            break
        action = menu.get(choice)
        if action:
            func = action[1]
            if func:
                func(mechanic)
        else:
            print("Invalid choice, try again.")

# --- Admin helper actions ---

def assign_job_logic():
    pending = [j for j in jobs if j.status == "Pending" and j.mechanic is None]
    if not pending:
        print("No pending jobs to assign.")
        return

    print("\nPending Jobs:")
    for i, job in enumerate(pending, start=1):
        print(f"{i}. {job.summary()}")

    try:
        sel = int(input("Select job number to assign: ")) - 1
        job = pending[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    mechanics = [u for u in users if isinstance(u, Mechanic)]
    if not mechanics:
        print("No mechanics available.")
        return

    print("\nMechanics:")
    for i, m in enumerate(mechanics, start=1):
        print(f"{i}. {m.username}")

    try:
        mech = mechanics[int(input("Select mechanic number: ")) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Prevent scheduling conflict
    for aj in mech.assigned_jobs:
        if aj.date == job.date and aj.time == job.time:
            print(f"\nCannot assign — {mech.username} already booked on {job.date} at {job.time}.")
            return

    job.mechanic = mech
    mech.assigned_jobs.append(job)
    job.status = "In Progress"
    print("Assigned job:", job.summary())

def generate_report_logic():
    total = len(jobs)
    pending = sum(1 for j in jobs if j.status == "Pending")
    in_prog = sum(1 for j in jobs if j.status == "In Progress")
    completed = sum(1 for j in jobs if j.status == "Completed")

    print("\n--- Service Job Report ---")
    print(f"Total jobs   : {total}")
    print(f"Pending      : {pending}")
    print(f"In Progress  : {in_prog}")
    print(f"Completed    : {completed}")

    mechanics = [u for u in users if isinstance(u, Mechanic)]
    if mechanics:
        print("\nJobs per mechanic:")
        for m in mechanics:
            print(f"  {m.username}: {len(m.assigned_jobs)}")
    else:
        print("\nNo mechanics registered.")
    print("---------------------------\n")

def view_customers():
    customers = [u for u in users if isinstance(u, Customer)]
    if not customers:
        print("\nNo customers registered.\n")
        return

    print("\n--- Customer Records ---")
    for c in customers:
        print(f"Username : {c.username}")
        print(f"Jobs     : {len(c.jobs)}")
        for j in c.jobs:
            print("  -", j.summary())
        print()
    print("------------------------\n")

def delete_customer():
    customers = [u for u in users if isinstance(u, Customer)]
    if not customers:
        print("No customers to delete.")
        return

    for i, c in enumerate(customers, start=1):
        print(f"{i}. {c.username}")

    try:
        sel = int(input("Select customer number to delete: ")) - 1
        cust = customers[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    confirm = input(f"Delete customer '{cust.username}' and all their jobs? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    global jobs
    jobs = [j for j in jobs if j.customer != cust]
    for m in (u for u in users if isinstance(u, Mechanic)):
        m.assigned_jobs = [j for j in m.assigned_jobs if j.customer != cust]
    users.remove(cust)
    print(f"Customer '{cust.username}' deleted with all their jobs.\n")

def create_invoice():
    completed = [j for j in jobs if j.status == "Completed" and not hasattr(j, 'invoice')]
    if not completed:
        print("No completed jobs pending invoice.")
        return

    for i, job in enumerate(completed, start=1):
        print(f"{i}. {job.summary()}")

    try:
        sel = int(input("Select job to create invoice for: ")) - 1
        job = completed[sel]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    job.invoice = Invoice(job)
    print("Invoice created for job:", job.summary())

def view_invoices_feedback():
    inv_jobs = [j for j in jobs if hasattr(j, 'invoice')]
    if not inv_jobs:
        print("No invoices found.")
        return

    for i, job in enumerate(inv_jobs, start=1):
        fb = job.invoice.feedback or "(no feedback)"
        print(f"{i}. Job: {job.summary()} — Feedback: {fb}")

    sel = input("Enter invoice number to view details (or press Enter to go back): ").strip()
    if not sel:
        return
    try:
        idx = int(sel) - 1
        job = inv_jobs[idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    print("\n--- Invoice Detail ---")
    inv = job.invoice
    print("Job:     ", job.summary())
    print("Feedback:", inv.feedback or "(none)")
    print("----------------------\n")

def admin_actions(admin: Admin):
    menu = {
        "1": ("Assign Job", assign_job_logic),
        "2": ("Generate Report", generate_report_logic),
        "3": ("View Customer Records", view_customers),
        "4": ("Delete Customer", delete_customer),
        "5": ("Create Invoice", create_invoice),
        "6": ("View Invoices / Feedback", view_invoices_feedback),
        "7": ("Logout", None),
    }
    while True:
        print("\n--- Admin Menu ---")
        for k, (desc, _) in menu.items():
            print(f"{k}. {desc}")
        choice = input("Select: ").strip()
        if choice == "7":
            break
        entry = menu.get(choice)
        if entry:
            func = entry[1]
            if func:
                func()
        else:
            print("Invalid choice, try again.")

# --- Main Application Loop ---

def main():
    menu = {
        "1": ("Register Customer", register_customer),
        "2": ("Login as Customer", lambda: _login_and_run("customer", customer_actions)),
        "3": ("Login as Mechanic", lambda: _login_and_run("mechanic", mechanic_actions)),
        "4": ("Login as Admin", lambda: _login_and_run("admin", admin_actions)),
        "5": ("Exit", None),
    }

    while True:
        print("\n--- Main Menu ---")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
        choice = input("Select: ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        entry = menu.get(choice)
        if not entry:
            print("Invalid choice, try again.")
            continue

        action = entry[1]
        if action:
            action()

def _login_and_run(role, action_func):
    user = login(role)
    if user:
        action_func(user)

if __name__ == "__main__":
    main()
