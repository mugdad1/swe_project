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

<<<<<<< HEAD
=======
def is_valid_time(time_str):
    """Check if the time string is valid format HH:MM."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

>>>>>>> f777f92 (jj)
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
    while True:
        print("\nCustomer Menu: 1-Book Service, 2-View My Jobs, 3-Logout")
        choice = input("Select: ")
        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            if not is_valid_date(date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            time = input("Time (HH:MM): ")
<<<<<<< HEAD
            # You can also validate time but for simplicity we skip it
=======
            if not is_valid_time(time):
                print("Invalid time format. Please use HH:MM.")
                continue
>>>>>>> f777f92 (jj)
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

def admin_actions(admin):
    while True:
        print("\nAdmin Menu: 1-Assign Job, 2-Generate Report, 3-Logout")
        choice = input("Select: ")
        if choice == "1":
            if not jobs:
                print("No jobs to assign")
                continue
            print("\nJobs:")
            for i, j in enumerate(jobs):
                assigned = j.mechanic.username if j.mechanic else "Unassigned"
                print(f"{i + 1}. {j.summary()} (Assigned to: {assigned})")

            try:
                sel = int(input("Select job number to assign: ")) - 1
                if not (0 <= sel < len(jobs)):
                    print("Invalid job number")
                    continue
            except ValueError:
                print("Invalid input, please enter a number")
                continue

            job = jobs[sel]

            mechanics = [u for u in users if u.role == "mechanic"]
            if not mechanics:
                print("No mechanics available")
                continue

            print("\nMechanics:")
            for mi, m in enumerate(mechanics):
                print(f"{mi + 1}. {m.username}")

            try:
                ms = int(input("Select mechanic number: ")) - 1
                if not (0 <= ms < len(mechanics)):
                    print("Invalid mechanic number")
                    continue
            except ValueError:
                print("Invalid input, please enter a number")
                continue

            mech = mechanics[ms]

            # Assign mechanic to job
            job.mechanic = mech
            if job not in mech.assigned_jobs:
                mech.assigned_jobs.append(job)

            print("Assigned job:", job.summary())

        elif choice == "2":
            print("\n=== All Jobs Report ===")
            for j in jobs:
                print(" -", j.summary())

            for mech in [u for u in users if u.role == "mechanic"]:
                print(f"\nMechanic: {mech.username} - Assigned Jobs")
                if not mech.assigned_jobs:
                    print(" - No jobs assigned")
                for j in mech.assigned_jobs:
                    print("   -", j.summary())
        elif choice == "3":
            break
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
