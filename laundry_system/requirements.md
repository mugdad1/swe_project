# Laundry Service Management System \- Requirements Document

## 1\. Introduction

This document describes the Laundry Service Management System, a college software project that streamlines laundry operations including appointment booking, task assignment, and reporting. The system is organized into three layers: user interface, business logic, and data persistence.

| Layer | Description |
| :---- | :---- |
| User Interface | CLI menus for customers, washers, and admins |
| Business Logic | Booking, updates, assignments, validations |
| Data Persistence | In-memory storage (RAM) |

---

## 2\. User Types and Responsibilities

| User Type | Responsibilities |
| :---- | :---- |
| Customer | Sign Up/Login, Book Service, Track Status, View History |
| Washer | Login, See Tasks, Update Status, Add Notes |
| Admin | Login, Manage Customers, Manage Appointments, Assign Work, View Reports/Create Invoices |

---

## 3\. Functional Requirements

### Customer FR

| FR | Requirement | Description |
| :---- | :---- | :---- |
| FR1 | Sign Up and Login | Customers can create a new account with name, email, and password. System validates email format and checks for duplicates. Customers can log in with their credentials. Password is hidden during input for security. |
| FR2 | Book a Service | Customers can book a laundry appointment by selecting a date (YYYY-MM-DD format) and time (HH:MM format). They choose service type (Wash, Iron, or Wash & Iron), enter item count and item types (e.g., 3 shirts, 2 pants). System calculates total price and shows it. Customer selects payment method (Credit Card, IBAN Transfer, or STC Pay). IBAN and STC Pay details are displayed for those payment options. |
| FR3 | Track Status | Customers can view all their appointments and see current status (Pending, In Progress, Completed). They can view detailed appointment information including task ID, task status, and washer notes. |
| FR4 | View History | Customers can view all their past and current laundry orders in one list. They can see which appointments are completed. |
| FR5 | View Appointment Payment Status | Customers can view payment method and payment status (Pending or Paid) for each appointment. |

### Washer FR

| FR | Requirement | Description |
| :---- | :---- | :---- |
| FR6 | Login | Washers can log in with their washer ID to access the system. |
| FR7 | See Tasks | Washers can view all tasks assigned to them by the admin. |
| FR8 | Update Status | Washers can update the status of their assigned tasks (Not Started → In Progress → Done). System verifies that the task is actually assigned to that washer before allowing update. |
| FR9 | Add Notes | Washers can add notes to their assigned tasks (e.g., "Delicate fabric \- use mild detergent"). System verifies that the task is assigned to that washer before allowing notes. |

### Admin FR

| FR | Requirement | Description |
| :---- | :---- | :---- |
| FR10 | Login | Admins can log in with admin password to access the system. |
| FR11 | Manage Customers | Admins can view all registered customer accounts and delete customer accounts. |
| FR12 | Manage Appointments | Admins can view all appointments, cancel any appointment, mark an appointment as Paid, and mark an appointment as Completed. |
| FR13 | Manage Washers | Admins can view all washers, add new washers, and delete washers. |
| FR14 | Assign Work | Admins can view available appointments (those without tasks), create a task from an appointment, select a washer to assign the task to, and link the task to both the appointment and washer. |
| FR15 | View Reports and Create Invoices | Admins can view reports showing total appointments with status breakdown (Completed, Pending, In Progress), view completed tasks, view pending tasks, and generate customer invoices showing all appointments with service details and total cost calculation. |

---

## 4\. Non-Functional Requirements

| NFR | Requirement | Description |
| :---- | :---- | :---- |
| NFR1 | Performance | The system shall respond quickly to provide a smooth user experience. |
| NFR2 | Security | The system shall implement role-based access control to restrict data access to authorized users. |
| NFR3 | Usability | The system should be easy to use for all user types with clear menus and prompts. |
| NFR4 | Data Storage | The system shall store all customer and appointment data in memory (RAM). |
| NFR5 | Maintainability | The code should be organized into separate modules and easy to understand for future updates. |

---

## 5\. Service Types and Pricing

| Service Type | Price (SR) |
| :---- | :---- |
| Wash | 10 |
| Iron | 5 |
| Wash & Iron | 15 |

---

## 6\. Payment Methods

| Method | Description |
| :---- | :---- |
| Credit Card | Card payment |
| IBAN Transfer | Bank transfer to account SA12 3456 7890 1234 5678 9012 34 (Saudi National Bank) |
| STC Pay | Mobile payment to \+966 50 123 4567 |

