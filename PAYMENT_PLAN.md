# Laundry System - Payment System Implementation Plan

## Overview
Add a payment system to the existing laundry management CLI application. Customers choose a payment method when booking, and admins can view payment details and update payment status.

---

## 1. Data Models (`classes.py`)

### Appointment Class Updates
Add two new fields:
- `payment_method: str` - The chosen payment method ("Cash", "Credit Card", "IBAN Transfer", "STC Pay")
- `payment_status: str` - Payment status ("Pending", "Paid")

---

## 2. Payment Configuration (`data.py`)

### Constants
```python
PAYMENT_METHODS = {
    "1": "Cash",
    "2": "Credit Card",
    "3": "IBAN Transfer",
    "4": "STC Pay"
}

FAKE_PAYMENT_DETAILS = {
    "iban": "SA12 3456 7890 1234 5678 9012 34",
    "stc_pay": "+966 50 123 4567"
}
```

---

## 3. Customer Flow (`customer_menu.py`)

### Modified `book_service()` Function
1. After selecting date/time
2. Display payment method menu
3. Customer selects option (1-4)
4. If "IBAN Transfer" → show fake IBAN
5. If "STC Pay" → show STC Pay number
6. Save `payment_method` and `payment_status="Pending"` to appointment

### Payment Method Menu Display
```
Choose payment method:
1. Cash (on delivery)
2. Credit Card
3. IBAN Transfer
4. STC Pay
```

### Fake Details Display
```
--- IBAN Transfer ---
Please transfer to: SA12 3456 7890 1234 5678 9012 34
---------------------

--- STC Pay ---
Send to: +966 50 123 4567
-----------
```

---

## 4. Admin Flow (`admin_menu.py`)

### Updated Appointment Display
Show payment method and status in appointment details:
```
Appointment ID: 1
Date: 2024-01-15
Time: 10:00
Status: Pending
Payment Method: IBAN Transfer
Payment Status: Pending
```

### New Admin Option: Mark as Paid
Add option in appointment management to change `payment_status` from "Pending" to "Paid".

### Updated `view_appointments()` Display
Include payment method and status in the appointment list view.

---

## 5. Files Summary

| File | Changes |
|------|---------|
| `classes.py` | Add `payment_method` and `payment_status` fields to Appointment class |
| `data.py` | Add `PAYMENT_METHODS` dict and `FAKE_PAYMENT_DETAILS` dict |
| `customer_menu.py` | Modify `book_service()` to prompt for payment method and show details |
| `admin_menu.py` | Update appointment views to show payment info; add "Mark as Paid" option |

---

## Implementation Order
1. Update `classes.py` - Add new fields to Appointment
2. Update `data.py` - Add payment constants
3. Update `customer_menu.py` - Add payment selection flow
4. Update `admin_menu.py` - Add payment display and status update
