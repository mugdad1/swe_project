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
    def init(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Customer(User):
    def init(self, username, password):
        super().init(username, password, "customer")
        self.jobs = []

class Mechanic(User):
    def init(self, username, password):
        super().init(username, password, "mechanic")
        self.assigned_jobs = []

class Admin(User):
    def init(self, username, password):
        super().init(username, password, "admin")

class ServiceJob:
    def init(self, customer, date, time):
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
    def init(self, job):
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
# -------------------- GUI RANGE START --------------------
# The GUI code below is self-contained and calls your existing functions/classes/data.
# It will run by default when the file is executed. The CLI (main) remains available.
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def run_gui():
    """Start the simple tkinter GUI (600x450). Uses the same users/jobs data structures."""
    root = tk.Tk()
    root.title("Service System GUI")
    root.geometry("600x450")
    root.resizable(True, True)

    # --- Helpers that operate on the same data structures (users, jobs, classes) ---
    def refresh_tree(tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", tk.END, values=row)

    def open_dashboard_for(user):
        """Open a simple role-specific window (popups + small tables)."""
        win = tk.Toplevel(root)
        win.title(f"{user.role.capitalize()} - {user.username}")
        win.geometry("620x420")

        header = ttk.Frame(win)
        header.pack(fill="x", pady=6, padx=6)
        ttk.Label(header, text=f"{user.role.capitalize()} : {user.username}", font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Button(header, text="Close", command=win.destroy).pack(side="right")

        body = ttk.Frame(win)
        body.pack(fill="both", expand=True, padx=8, pady=8)

        # Left buttons frame
        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0,8))

        # Right area: treeview or text
        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True)

        # For job lists display
        cols_common = ("cust","date","time","status","mech","comments")
        tree = ttk.Treeview(right, columns=cols_common, show="headings", height=15)
        for c,w in [("cust",120),("date",90),("time",70),("status",110),("mech",100),("comments",200)]:
            tree.heading(c, text=c.title()); tree.column(c, width=w)
        tree.pack(fill="both", expand=True)

        # ---------- Customer UI ----------
        if user.role == "customer":
            ttk.Button(left, text="Book Service", width=20, command=lambda: gui_book_service(user, tree)).pack(pady=6)
            ttk.Button(left, text="My Jobs", width=20, command=lambda: gui_show_customer_jobs(user, tree)).pack(pady=6)
            ttk.Button(left, text="Change Password", width=20, command=lambda: gui_change_password(user)).pack(pady=6)
            ttk.Button(left, text="Delete Account", width=20, command=lambda: gui_delete_account(user, win)).pack(pady=6)
            ttk.Button(left, text="Add Feedback", width=20, command=lambda: gui_add_feedback(user)).pack(pady=6)
            gui_show_customer_jobs(user, tree)

        # ---------- Mechanic UI ----------
        elif user.role == "mechanic":
            ttk.Button(left, text="View My Jobs", width=20, command=lambda: gui_show_mechanic_jobs(user, tree)).pack(pady=6)
            ttk.Button(left, text="Update Job Status", width=20, command=lambda: gui_update_mechanic_job(user, tree)).pack(pady=6)
            gui_show_mechanic_jobs(user, tree)

        # ---------- Admin UI ----------
        elif user.role == "admin":
            ttk.Button(left, text="Assign Job", width=20, command=lambda: gui_assign_job(tree)).pack(pady=6)
            ttk.Button(left, text="Generate Report", width=20, command=gui_generate_report).pack(pady=6)
            ttk.Button(left, text="View Customers", width=20, command=gui_view_customers).pack(pady=6)
            ttk.Button(left, text="Delete Customer", width=20, command=lambda: gui_delete_customer(tree)).pack(pady=6)
            ttk.Button(left, text="Create Invoice", width=20, command=lambda: gui_create_invoice(tree)).pack(pady=6)
            ttk.Button(left, text="View Invoices/Feedback", width=20, command=gui_view_invoices).pack(pady=6)
            gui_update_admin_tree(tree)
# ---------- GUI action implementations (use same data structures) ----------
    def gui_book_service(customer, tree=None):
        date = simpledialog.askstring("Date", "Date (YYYY-MM-DD):", parent=root)
        if not date or not is_valid_date(date):
            messagebox.showerror("Error", "Invalid date.")
            return
        time = simpledialog.askstring("Time", "Time (HH:MM):", parent=root)
        if not time or not is_valid_time(time):
            messagebox.showerror("Error", "Invalid time.")
            return
        if any(j.date == date and j.time == time for j in customer.jobs):
            messagebox.showerror("Error", "You already have a booking at that date/time.")
            return
        job = ServiceJob(customer, date, time)
        jobs.append(job); customer.jobs.append(job)
        messagebox.showinfo("Booked", "Service booked.")
        if tree:
            gui_show_customer_jobs(customer, tree)

    def gui_show_customer_jobs(customer, tree):
        rows = []
        for j in customer.jobs:
            mech = j.mechanic.username if j.mechanic else ""
            rows.append((j.customer.username, j.date, j.time, j.status, mech, j.comments))
        refresh_tree(tree, rows)

    def gui_change_password(user):
        current = simpledialog.askstring("Current Password", "Enter current password:", show="*", parent=root)
        if current != user.password:
            messagebox.showerror("Error", "Incorrect password.")
            return
        new_pw = simpledialog.askstring("New Password", "Enter new password:", show="*", parent=root)
        confirm = simpledialog.askstring("Confirm Password", "Confirm new password:", show="*", parent=root)
        if new_pw != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not new_pw or not new_pw.strip():
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        user.password = new_pw
        messagebox.showinfo("Success", "Password updated successfully.")

    def gui_delete_account(user, parent_win):
        pw = simpledialog.askstring("Confirm", "Enter your password to confirm deletion:", show="*", parent=parent_win)
        if pw != user.password:
            messagebox.showerror("Error", "Incorrect password.")
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
            return
        global jobs, users
        jobs = [job for job in jobs if job.customer != user]
        for m in (u for u in users if isinstance(u, Mechanic)):
            m.assigned_jobs = [j for j in m.assigned_jobs if j.customer != user]
        users.remove(user)
        messagebox.showinfo("Deleted", "Account deleted.")
        parent_win.destroy()

    def gui_add_feedback(customer):
        completed = [job for job in customer.jobs if job.status == "Completed" and job.invoice]
        if not completed:
            messagebox.showinfo("Info", "No completed jobs with invoice.")
            return
        choices = [f"{i+1}. {j.summary()}" for i,j in enumerate(completed)]
        sel = simpledialog.askinteger("Select job", "\n".join(choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(completed))
        if not sel: return
        job = completed[sel-1]
        fb = simpledialog.askstring("Feedback", "Enter feedback:", parent=root)
        job.invoice.feedback = fb
        messagebox.showinfo("Done", "Feedback added.")

    def gui_show_mechanic_jobs(mech, tree):
        rows = []
        for j in mech.assigned_jobs:
            rows.append((j.customer.username, j.date, j.time, j.status, j.mechanic.username if j.mechanic else "", j.comments))
        refresh_tree(tree, rows)

    def gui_update_mechanic_job(mech, tree):
if not mech.assigned_jobs:
            messagebox.showinfo("Info", "No assigned jobs.")
            return
        choices = [f"{i+1}. {j.summary()}" for i,j in enumerate(mech.assigned_jobs)]
        sel = simpledialog.askinteger("Select job", "\n".join(choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(mech.assigned_jobs))
        if not sel: return
        job = mech.assigned_jobs[sel-1]
        status = simpledialog.askstring("Status", "New status (Pending/In Progress/Completed):", parent=root)
        if status is None: return
        status = status.title()
        if status not in {"Pending", "In Progress", "Completed"}:
            messagebox.showerror("Error", "Invalid status.")
            return
        job.status = status
        job.comments = simpledialog.askstring("Comments", "Comments (optional):", parent=root) or ""
        messagebox.showinfo("Done", "Job updated.")
        if tree:
            gui_show_mechanic_jobs(mech, tree)

    def gui_update_admin_tree(tree):
        rows = []
        for j in jobs:
            mech = j.mechanic.username if j.mechanic else ""
            rows.append((j.customer.username, j.date, j.time, j.status, mech, j.comments))
        refresh_tree(tree, rows)

    def gui_assign_job(tree=None):
        pending = [j for j in jobs if j.status == "Pending" and j.mechanic is None]
        if not pending:
            messagebox.showinfo("Info", "No pending jobs.")
            return
        choices = [f"{i+1}. {j.summary()}" for i,j in enumerate(pending)]
        sel = simpledialog.askinteger("Select job", "\n".join(choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(pending))
        if not sel: return
        job = pending[sel-1]
        mechanics = [u for u in users if isinstance(u, Mechanic)]
        if not mechanics:
            messagebox.showinfo("Info", "No mechanics available.")
            return
        mech_choices = [f"{i+1}. {m.username}" for i,m in enumerate(mechanics)]
        msel = simpledialog.askinteger("Select mechanic", "\n".join(mech_choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(mechanics))
        if not msel: return
        mech = mechanics[msel-1]
        # prevent conflict
        for aj in mech.assigned_jobs:
            if aj.date == job.date and aj.time == job.time:
                messagebox.showerror("Error", f"{mech.username} already booked at that time.")
                return
        job.mechanic = mech; mech.assigned_jobs.append(job); job.status = "In Progress"
        messagebox.showinfo("Assigned", "Job assigned.")
        if tree:
            gui_update_admin_tree(tree)

    def gui_generate_report():
        total = len(jobs); pending = sum(1 for j in jobs if j.status=="Pending")
        in_prog = sum(1 for j in jobs if j.status=="In Progress"); completed = sum(1 for j in jobs if j.status=="Completed")
        s = (f"Total: {total}\nPending: {pending}\nIn Progress: {in_prog}\nCompleted: {completed}\n\n")
        mechs = [u for u in users if isinstance(u, Mechanic)]
        for m in mechs:
            s += f"{m.username}: {len(m.assigned_jobs)} jobs\n"
        messagebox.showinfo("Report", s)

    def gui_view_customers():
        customers = [u for u in users if isinstance(u, Customer)]
        if not customers:
            messagebox.showinfo("Info", "No customers registered.")
            return
        s = ""
        for c in customers:
            s += f"Username: {c.username}\nJobs: {len(c.jobs)}\n"
            for j in c.jobs:
                s += "  - " + j.summary() + "\n"
            s += "\n"
        dlg = tk.Toplevel(root); dlg.title("Customer Records")
        txt = tk.Text(dlg, width=100, height=30); txt.pack(fill="both", expand=True)
        txt.insert(tk.END, s)

    def gui_delete_customer(tree=None):
customers = [u for u in users if isinstance(u, Customer)]
        if not customers:
            messagebox.showinfo("Info", "No customers to delete.")
            return
        choices = [f"{i+1}. {c.username} ({len(c.jobs)} jobs)" for i,c in enumerate(customers)]
        sel = simpledialog.askinteger("Select customer", "\n".join(choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(customers))
        if not sel: return
        cust = customers[sel-1]
        if not messagebox.askyesno("Confirm", f"Delete customer '{cust.username}' and all their jobs?"):
            return
        global jobs
        jobs = [j for j in jobs if j.customer != cust]
        for m in (u for u in users if isinstance(u, Mechanic)):
            m.assigned_jobs = [j for j in m.assigned_jobs if j.customer != cust]
        users.remove(cust)
        messagebox.showinfo("Deleted", f"Customer '{cust.username}' deleted.")
        if tree:
            gui_update_admin_tree(tree)

    def gui_create_invoice(tree=None):
        completed_no_inv = [j for j in jobs if j.status=="Completed" and not j.invoice]
        if not completed_no_inv:
            messagebox.showinfo("Info", "No completed jobs pending invoice.")
            return
        choices = [f"{i+1}. {j.summary()}" for i,j in enumerate(completed_no_inv)]
        sel = simpledialog.askinteger("Select job", "\n".join(choices)+"\nEnter number:", parent=root, minvalue=1, maxvalue=len(completed_no_inv))
        if not sel: return
        job = completed_no_inv[sel-1]
        job.invoice = Invoice(job)
        messagebox.showinfo("Done", "Invoice created.")
        if tree:
            gui_update_admin_tree(tree)

    def gui_view_invoices():
        inv_jobs = [j for j in jobs if j.invoice]
        if not inv_jobs:
            messagebox.showinfo("Info", "No invoices found.")
            return
        s = ""
        for i,j in enumerate(inv_jobs, start=1):
            fb = j.invoice.feedback or "(no feedback)"
            s += f"{i}. Job: {j.summary()} — Feedback: {fb}\n"
        dlg = tk.Toplevel(root); dlg.title("Invoices & Feedback")
        txt = tk.Text(dlg, width=100, height=30); txt.pack(fill="both", expand=True)
        txt.insert(tk.END, s)

    # ------------------ Main Login Window ------------------
    main_frame = ttk.Frame(root, padding=12)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Service System", font=("Segoe UI", 18, "bold")).pack(pady=(4,8))

    lf = ttk.LabelFrame(main_frame, text="Login", padding=10)
    lf.pack(pady=6, padx=6, fill="x")

    ttk.Label(lf, text="Role:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
    role_var = tk.StringVar(value="customer")
    role_combo = ttk.Combobox(lf, textvariable=role_var, state="readonly", values=["customer","mechanic","admin"], width=14)
    role_combo.grid(row=0, column=1, padx=6, pady=6, sticky="w")

    ttk.Label(lf, text="Username:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    uname_entry = ttk.Entry(lf); uname_entry.grid(row=1, column=1, padx=6, pady=6, sticky="w")

    ttk.Label(lf, text="Password:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
    pw_entry = ttk.Entry(lf, show="*"); pw_entry.grid(row=2, column=1, padx=6, pady=6, sticky="w")

    def attempt_login():
        role = role_var.get()
        uname = uname_entry.get().strip()
        pw = pw_entry.get()
        user = find_user(uname)
        if not user or user.password != pw or user.role != role:
            messagebox.showerror("Login failed", "Invalid credentials or role.")
            return
        uname_entry.delete(0, tk.END); pw_entry.delete(0, tk.END)
        open_dashboard_for(user)

    ttk.Button(lf, text="Login", command=attempt_login).grid(row=3, column=0, columnspan=2, pady=8)
    ttk.Button(main_frame, text="Register Customer", command=lambda: open_register()).pack(pady=(6,2))

    ttk.Label(main_frame, text="Default accounts: admin/admin, mech1/mech1, mech2/mech2", foreground="gray").pack(pady=(6,0))
# Register popup
    def open_register():
        dlg = tk.Toplevel(root); dlg.title("Register Customer")
        dlg.geometry("360x180")
        ttk.Label(dlg, text="Username:").pack(pady=(10,0))
        u_e = ttk.Entry(dlg); u_e.pack(pady=4)
        ttk.Label(dlg, text="Password:").pack(pady=(6,0))
        p_e = ttk.Entry(dlg, show="*"); p_e.pack(pady=4)
        def do_create():
            username = u_e.get().strip(); password = p_e.get()
            if not username:
                messagebox.showerror("Error", "Username cannot be empty."); return
            if find_user(username):
                messagebox.showerror("Error", "Username already exists."); return
            if not password.strip():
                messagebox.showerror("Error", "Password cannot be empty."); return
            users.append(Customer(username, password))
            messagebox.showinfo("Success", f"Customer '{username}' created.")
            dlg.destroy()
        ttk.Button(dlg, text="Create", command=do_create).pack(pady=10)

    root.mainloop()

# -------------------- GUI RANGE END ----------------------

# At the end: keep main() intact; run GUI by default but fallback to CLI if GUI fails.
if name == "main":
    try:
        run_gui()
    except Exception as e:
        print("GUI failed to start or crashed. Falling back to CLI.")
        print("Error:", e)
        main()
