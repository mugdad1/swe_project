# Laundry System - Enhancement Plan

## Overview
This plan covers three improvements to the laundry management CLI application:
1. Show washer notes in customer appointment details
2. Add service type selection with item count/details
3. Fix admin reports UI (add clear_screen/pause)

---

## Issue 1: Show Washer Notes in Customer View

### Problem
Customer cannot see washer notes when viewing appointment details.

### Current State (`customer_menu.py:162-171`)
```python
if apt:
    print(f"\nAppointment ID: {apt.appointment_id}")
    print(f"Date: {apt.date}")
    print(f"Time: {apt.time}")
    print(f"Status: {apt.status}")
    if apt.task_id:
        print(f"Task ID: {apt.task_id}")
    print(f"Payment Method: {apt.payment_method}")
    print(f"Payment Status: {apt.payment_status}")
```

### Fix (`customer_menu.py` → `view_appointment_details()`)
After printing `Task ID`, fetch the task and display:
- Task description
- Task status
- Washer notes (if any)

### New Output Example
```
Appointment ID: 1
Date: 2024-04-20
Time: 10:00
Status: Pending
Task ID: 1
  Description: Wash & Iron
  Status: In Progress
  Notes: Delicate fabric - used mild detergent
Payment Method: IBAN Transfer
Payment Status: Pending
```

---

## Issue 2: Service Type and Item Details

### Problem
Customer only picks date/time. No service details or item information.

### 2.1 Update Data Model (`classes.py`)

Add three new fields to `Appointment` class:
```python
def __init__(
    self,
    appointment_id: int,
    customer_id: int,
    date: str,
    time: str,
    status: str = "Pending",
    payment_method: str = "Cash",
    payment_status: str = "Pending",
    service_type: str = "Wash",
    item_count: int = 0,
    item_types: str = "",
) -> None:
    # ... existing fields ...
    self.service_type: str = service_type
    self.item_count: int = item_count
    self.item_types: str = item_types
```

### 2.2 Add Service Constants (`data.py`)

```python
SERVICE_TYPES = {
    "1": "Wash",
    "2": "Dry Clean",
    "3": "Iron",
    "4": "Wash & Iron",
    "5": "Express Service",
    "6": "Other"
}
```

### 2.3 Update Customer Flow (`customer_menu.py` → `book_service()`)

**New Booking Flow:**
```
=== Book a Service ===
Enter date (YYYY-MM-DD): [input]
Enter time (HH:MM): [input]

=== Select Service ===
1. Wash
2. Dry Clean
3. Iron
4. Wash & Iron
5. Express Service
6. Other (custom)

Enter your choice (1-6): [input]

# If "Other" selected:
Enter custom service description: [free text input]

How many pieces? [number input]

Enter item types (e.g., T-shirts, Pants, Dresses):
[free text input - e.g., "3 T-shirts, 2 jeans, 1 jacket"]

=== Choose Payment Method ===
1. Cash (on delivery)
2. Credit Card
3. IBAN Transfer
4. STC Pay

Enter your choice (1-4): [input]
```

**Code Changes:**
1. Import `SERVICE_TYPES` from `data.py`
2. After date/time input, show service menu
3. Handle service choice (1-6)
4. If "Other", prompt for custom description
5. Prompt for item count and item types
6. THEN show payment method selection
7. Save all fields to appointment

### 2.4 Update Admin Display (`admin_menu.py`)

**In `assign_tasks()` - Show service info:**
```python
for apt in available_apts:
    print(
        f"ID: {apt.appointment_id}, Customer: {apt.customer_id}, "
        f"Service: {apt.service_type}, Items: {apt.item_count} - {apt.item_types}, "
        f"Date: {apt.date}, Payment: {apt.payment_method} ({apt.payment_status})"
    )
```

**In `view_reports()` - Invoice includes service:**
```python
for apt in customer_apts:
    cost = 50
    print(
        f"  - Appointment {apt.appointment_id}: {apt.date} "
        f"Service: {apt.service_type} ({apt.item_count} pcs - {apt.item_types}) "
        f"Status: {apt.status} - Payment: {apt.payment_method} ({apt.payment_status}) "
        f"Cost: ${cost}"
    )
```

---

## Issue 3: Admin Reports UI Fix

### Problem
`view_reports()` lacks `clear_screen()` and `pause()` - results flash without proper display.

### Fix (`admin_menu.py` → `view_reports()`)

Add at function start:
```python
def view_reports() -> None:
    clear_screen()  # ADD THIS
    print("\n=== Reports ===")
    # ... rest of function ...

    if choice == "1":
        # ... print report ...
        pause()  # ADD THIS after each report
    elif choice == "2":
        # ... print report ...
        pause()  # ADD THIS
    elif choice == "3":
        # ... print report ...
        pause()  # ADD THIS
    elif choice == "4":
        # ... print report ...
        pause()  # ADD THIS
```

---

## Files to Modify

| File | Changes |
|-------|---------|
| `classes.py` | Add `service_type`, `item_count`, `item_types` to Appointment |
| `data.py` | Add `SERVICE_TYPES` dict |
| `customer_menu.py` | 1. Add service selection flow 2. Add item count/types 3. Fix notes display |
| `admin_menu.py` | 1. Show service info in lists 2. Add clear_screen/pause to reports |

---

## Implementation Order

1. **`classes.py`** - Add service fields to Appointment
2. **`data.py`** - Add SERVICE_TYPES constant
3. **`customer_menu.py`** - Update book_service() with new flow
4. **`customer_menu.py`** - Fix view_appointment_details() to show notes
5. **`admin_menu.py`** - Update assign_tasks() display
6. **`admin_menu.py`** - Update view_reports() invoice
7. **`admin_menu.py`** - Add clear_screen/pause to view_reports()
8. **Test all changes**
9. **Update `testing.md`**

---

## Test Checklist

- [ ] Customer can select service type (1-6)
- [ ] Customer can enter custom service if "Other"
- [ ] Customer must enter item count and types
- [ ] Service info saved to appointment
- [ ] Customer can see washer notes in appointment details
- [ ] Admin sees service info when assigning tasks
- [ ] Admin invoice shows service details
- [ ] Reports display properly with clear_screen/pause
