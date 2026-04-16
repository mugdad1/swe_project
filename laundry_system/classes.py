from __future__ import annotations
from typing import Optional


class Customer:
    def __init__(self, customer_id: int, name: str, email: str, password: str) -> None:
        self.customer_id: int = customer_id
        self.name: str = name
        self.email: str = email
        self.password: str = password
        self.appointments: list[int] = []

    def __str__(self) -> str:
        return f"ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"


class Appointment:
    def __init__(
        self,
        appointment_id: int,
        customer_id: int,
        date: str,
        time: str,
        status: str = "Pending",
        payment_method: str = "Cash",
        payment_status: str = "Pending",
    ) -> None:
        self.appointment_id: int = appointment_id
        self.customer_id: int = customer_id
        self.date: str = date
        self.time: str = time
        self.status: str = status
        self.task_id: Optional[int] = None
        self.payment_method: str = payment_method
        self.payment_status: str = payment_status

    def __str__(self) -> str:
        return f"ID: {self.appointment_id}, Customer: {self.customer_id}, Date: {self.date}, Time: {self.time}, Status: {self.status}, Payment: {self.payment_method} ({self.payment_status})"


class Task:
    def __init__(
        self,
        task_id: int,
        appointment_id: int,
        description: str,
        status: str = "Not Started",
    ) -> None:
        self.task_id: int = task_id
        self.appointment_id: int = appointment_id
        self.description: str = description
        self.status: str = status
        self.notes: str = ""

    def __str__(self) -> str:
        return f"ID: {self.task_id}, Appointment: {self.appointment_id}, Description: {self.description}, Status: {self.status}"


class Washer:
    def __init__(self, washer_id: int, name: str) -> None:
        self.washer_id: int = washer_id
        self.name: str = name
        self.assigned_tasks: list[int] = []

    def __str__(self) -> str:
        return f"ID: {self.washer_id}, Name: {self.name}"
