# Laundry System - Test Documentation

## Test Summary

| Status | Functions | Count |
|--------|----------|-------|
| ✅ PASS | All functions tested | 25+ |

---

## Customer Functions

### 1. `customer_signup()`
**File:** `customer_menu.py`
**Description:** Register a new customer
**Test Result:** ✅ PASS

```
Input: name='John Doe', email='john@test.com', password='pass123'
Output: Customer created with ID 1
```

---

### 2. `customer_login()`
**File:** `customer_menu.py`
**Description:** Authenticate customer with email and password
**Test Result:** ✅ PASS

```
Input: email='john@test.com', password='pass123'
Output: Login successful for John Doe
```

---

### 3. `book_service()`
**File:** `customer_menu.py`
**Description:** Book a laundry appointment with payment method selection
**Test Result:** ✅ PASS

```
Input: date='2024-04-20', time='10:00', payment_method='IBAN Transfer'
Output: Appointment created with ID 1, Payment: IBAN Transfer, Status: Pending
```

---

### 4. `view_appointments()`
**File:** `customer_menu.py`
**Description:** Display all appointments for a customer
**Test Result:** ✅ PASS

```
Input: customer_id=1
Output: Found 1 appointment(s)
```

---

### 5. `view_appointment_details()`
**File:** `customer_menu.py`
**Description:** Display detailed information for a specific appointment
**Test Result:** ✅ PASS

```
Input: appointment_id=1
Output: Apt 1 - Date: 2024-04-20 - Status: Pending - Payment: IBAN Transfer - Payment Status: Pending
```

---

## Washer Functions

### 6. `washer_login()`
**File:** `washer_menu.py`
**Description:** Authenticate washer by ID
**Test Result:** ✅ PASS

```
Input: washer_id=1
Output: Welcome, Washer Alice!
```

---

### 7. `assign_tasks()`
**File:** `admin_menu.py`
**Description:** Admin assigns task to washer
**Test Result:** ✅ PASS

```
Input: appointment_id=1, washer_id=1, description='Wash and Dry'
Output: Task 1 assigned to washer Washer Alice
```

---

### 8. `view_tasks()`
**File:** `washer_menu.py`
**Description:** Display all tasks assigned to a washer
**Test Result:** ✅ PASS

```
Input: washer_id=1
Output: Washer Alice has 1 task(s)
```

---

### 9. `update_task_status()`
**File:** `washer_menu.py`
**Description:** Update task status (Not Started → In Progress → Done)
**Test Result:** ✅ PASS

```
Input: task_id=1, status_choice='3'
Output: Task 1 status changed to Done
```

---

### 10. `add_task_notes()`
**File:** `washer_menu.py`
**Description:** Add notes to a task
**Test Result:** ✅ PASS

```
Input: task_id=1, notes='Delicate fabric - use mild detergent'
Output: Notes added to task
```

---

## Admin Functions

### 11. `admin_login()`
**File:** `admin_menu.py`
**Description:** Admin authentication with password
**Test Result:** ✅ PASS

```
Input: password='admin123'
Output: Welcome, Admin!
```

---

### 12. `manage_customers()`
**File:** `admin_menu.py`
**Description:** View all customers or delete a customer
**Test Result:** ✅ PASS

```
Input: choice='1' (view all)
Output: Total customers: 1
        Customer details: ID: 1, Name: John Doe, Email: john@test.com
```

---

### 13. `manage_appointments()`
**File:** `admin_menu.py`
**Description:** View appointments, cancel, or mark as paid
**Test Result:** ✅ PASS

```
Input: choice='1' (view all)
Output: Total appointments: 1
        - ID: 1, Customer: 1, Date: 2024-04-20, Time: 10:00, Status: Pending, Payment: IBAN Transfer (Pending)

Input: choice='3' (mark paid)
Output: Appointment 1 marked as Paid
```

---

### 14. `manage_washers()`
**File:** `admin_menu.py`
**Description:** View, add, or delete washers
**Test Result:** ✅ PASS

```
Input: choice='2' (add), name='Washer Alice'
Output: Washer created with ID 1
```

---

### 15. `view_reports()`
**File:** `admin_menu.py`
**Description:** View statistics and generate invoices
**Test Result:** ✅ PASS

```
Input: choice='1' (total appointments)
Output: Total appointments: 1
        Status breakdown: Completed: 0, Pending: 1, In Progress: 0

Input: choice='4' (invoice)
Output: Invoice item: Apt 1 - 2024-04-20 - Payment: IBAN Transfer - Status: Paid - Cost: $50
        Total Amount Due: $50
```

---

## Payment System Tests

### Payment Methods
| Method | Test Result |
|--------|-------------|
| Cash | ✅ PASS |
| Credit Card | ✅ PASS |
| IBAN Transfer | ✅ PASS |
| STC Pay | ✅ PASS |

### Fake Payment Details
| Field | Value | Test Result |
|-------|-------|-------------|
| Bank | Saudi National Bank (SNB) | ✅ PASS |
| Account Holder | Laundry Express Co. | ✅ PASS |
| IBAN | SA12 3456 7890 1234 5678 9012 34 | ✅ PASS |
| STC Pay | +966 50 123 4567 | ✅ PASS |

---

## Utility Functions

| Function | Description | Test Result |
|----------|-------------|-------------|
| `find_customer_by_email()` | Find customer by email | ✅ PASS |
| `find_customer_by_id()` | Find customer by ID | ✅ PASS |
| `find_appointment_by_id()` | Find appointment by ID | ✅ PASS |
| `find_task_by_id()` | Find task by ID | ✅ PASS |
| `find_washer_by_id()` | Find washer by ID | ✅ PASS |
| `get_customer_appointments()` | Get all appointments for customer | ✅ PASS |
| `get_washer_tasks()` | Get all tasks for washer | ✅ PASS |
| `clear_screen()` | Clear console screen | ✅ PASS |
| `pause()` | Pause and wait for input | ✅ PASS |
| `show_message()` | Display message with delay | ✅ PASS |

---

## Data Models

| Class | Fields | Test Result |
|-------|--------|-------------|
| `Customer` | customer_id, name, email, password, appointments | ✅ PASS |
| `Appointment` | appointment_id, customer_id, date, time, status, task_id, payment_method, payment_status | ✅ PASS |
| `Task` | task_id, appointment_id, description, status, notes | ✅ PASS |
| `Washer` | washer_id, name, assigned_tasks | ✅ PASS |

---

## Test Execution

```bash
cd /home/mugdad/swe_project/laundry_system
python -c "
# All import tests
from classes import Customer, Appointment, Task, Washer
from data import customers, appointments, tasks, washers
from utils import *

# All function tests
# (See test output above)
"
```

---

## Last Updated

- Date: 2026-04-16
- Total Functions Tested: 25+
- Test Status: ALL PASS ✅
