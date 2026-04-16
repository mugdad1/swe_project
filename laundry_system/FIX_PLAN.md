# Fix Plan - Laundry System

## Issues Found During Testing

1. **`get_washer_tasks()` returns None in list** - Filter doesn't exclude None before returning
2. **No date/time validation** - Invalid dates/times accepted
3. **No price calculation** - Flat $50 used, no per-service pricing
4. **No email validation** - No format checking
5. **Washer can modify any task** - Only checks task_id in list, not actual ownership
6. **Customer cannot cancel appointments** - Need option in dashboard
7. **Admin cannot mark appointment completed** - No function to close completed tasks
8. **Admin UI flashes (no clear_screen/pause)** - Several admin functions need pauses
9. **Exit screens too fast** - Need pause before returning to main menu

---

## Fix Tasks

### 1. utils.py - Fix get_washer_tasks() None issue
- Filter out None values before returning

### 2. customer_menu.py - Add date/time validation
- Validate YYYY-MM-DD format
- Validate HH:MM format

### 3. admin_menu.py - Add price calculation
- Add SERVICE_PRICES dict
- Calculate based on service_type and item_count

### 4. customer_menu.py - Add email validation
- Basic email format check (contains @ and .)

### 5. washer_menu.py - Fix task verification
- Verify task is actually assigned to washer's tasks list
- Compare task_id against washer's assigned_tasks properly

### 6. customer_menu.py - Add cancel appointment
- Add option 5 in dashboard to cancel appointment

### 7. admin_menu.py - Add mark completed
- Add option to mark appointment as Completed when task is Done

### 8. admin_menu.py - Add clear_screen/pause
- Add to: manage_customers, manage_appointments, manage_washers, assign_tasks

### 9. main.py - Add pause before exit
- Add pause after each menu option before returning to main

---

## Implementation Order

1. utils.py - Fix get_washer_tasks()
2. customer_menu.py - Add validations + cancel option
3. admin_menu.py - Add price calculation + marking completed + clear_screen/pause
4. main.py - Add pause before exit
5. Run all tests and verify