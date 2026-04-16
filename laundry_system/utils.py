# Utility functions for common tasks
from __future__ import annotations
import time
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


def get_washer_tasks(washer_id: int) -> list[Task | None]:
    """Get all tasks assigned to a washer"""
    from data import washers

    washer = find_washer_by_id(washer_id)
    if washer:
        return [find_task_by_id(task_id) for task_id in washer.assigned_tasks]
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
