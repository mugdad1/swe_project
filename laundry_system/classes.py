# Customer Class
class Customer:
    def __init__(self, customer_id, name, email, password):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.password = password
        self.appointments = []  # List of appointment IDs

    def __str__(self):
        return f"ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"


# Appointment Class
class Appointment:
    def __init__(self, appointment_id, customer_id, date, time, status="Pending"):
        self.appointment_id = appointment_id
        self.customer_id = customer_id
        self.date = date
        self.time = time
        self.status = status  # Pending, In Progress, Completed
        self.task_id = None  # Will be assigned by admin

    def __str__(self):
        return f"ID: {self.appointment_id}, Customer: {self.customer_id}, Date: {self.date}, Time: {self.time}, Status: {self.status}"


# Task Class
class Task:
    def __init__(self, task_id, appointment_id, description, status="Not Started"):
        self.task_id = task_id
        self.appointment_id = appointment_id
        self.description = description
        self.status = status  # Not Started, In Progress, Done
        self.notes = ""  # Washer can add notes

    def __str__(self):
        return f"ID: {self.task_id}, Appointment: {self.appointment_id}, Description: {self.description}, Status: {self.status}"


# Washer Class
class Washer:
    def __init__(self, washer_id, name):
        self.washer_id = washer_id
        self.name = name
        self.assigned_tasks = []  # List of task IDs

    def __str__(self):
        return f"ID: {self.washer_id}, Name: {self.name}"
