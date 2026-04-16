# Utility functions for common tasks
from __future__ import annotations
import time
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes import Customer, Appointment, Task, Washer


def find_customer_by_email(email: str) -> Customer | None:
    """Find a customer by email"""
    from data import customers

    for customer in customers:
        if customer.email == email:
            return customer
    return None


def find_customer_by_id(customer_id: int) -> Customer | None:
    """Find a customer by ID"""
    from data import customers

    for customer in customers:
        if customer.customer_id == customer_id:
            return customer
    return None


def find_appointment_by_id(appointment_id: int) -> Appointment | None:
    """Find an appointment by ID"""
    from data import appointments

    for appointment in appointments:
        if appointment.appointment_id == appointment_id:
            return appointment
    return None


def find_task_by_id(task_id: int) -> Task | None:
    """Find a task by ID"""
    from data import tasks

    for task in tasks:
        if task.task_id == task_id:
            return task
    return None


def find_washer_by_id(washer_id: int) -> Washer | None:
    """Find a washer by ID"""
    from data import washers

    for washer in washers:
        if washer.washer_id == washer_id:
            return washer
    return None


def get_customer_appointments(customer_id: int) -> list[Appointment]:
    """Get all appointments for a customer"""
    from data import appointments

    return [apt for apt in appointments if apt.customer_id == customer_id]


def get_washer_tasks(washer_id: int) -> list[Task]:
    """Get all tasks assigned to a washer"""
    from data import washers

    washer = find_washer_by_id(washer_id)
    if washer:
        tasks = [find_task_by_id(task_id) for task_id in washer.assigned_tasks]
        return [t for t in tasks if t is not None]
    return []


def clear_screen():
    """Clear the console screen"""
    import os

    os.system("clear" if os.name == "posix" else "cls")


def pause():
    """Pause and wait for user input"""
    input("\nPress Enter to continue...")


def show_message(message, wait_time=2):
    """Show a message and wait"""
    print(f"\n{message}")
    time.sleep(wait_time)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_date(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD"""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    try:
        year, month, day = map(int, date_str.split("-"))
        if month < 1 or month > 12 or day < 1 or day > 31:
            return False
        if year < 2024:
            return False
        return True
    except:
        return False


def validate_time(time_str: str) -> bool:
    """Validate time format HH:MM"""
    pattern = r"^\d{2}:\d{2}$"
    if not re.match(pattern, time_str):
        return False
    try:
        hour, minute = map(int, time_str.split(":"))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return False
        return True
    except:
        return False


def get_int_input(prompt: str) -> int | None:
    """Safely get integer input - returns None if invalid"""
    try:
        return int(input(prompt))
    except ValueError:
        return None
