# Fix Plan - Laundry System

## Issues Found During Testing

| # | Issue | Status |
|---|-------|--------|
| 1 | get_washer_tasks() returns None in list | ✅ DONE |
| 2 | No date/time validation | ✅ DONE |
| 3 | No price calculation - Flat $50 | ✅ DONE |
| 4 | No email validation | ✅ DONE |
| 5 | Invalid email kicks user out | ✅ DONE |
| 6 | Password not showing asterisks | ✅ DONE |
| 7 | Washer can modify any task | ✅ DONE |
| 8 | Customer cannot cancel appointments | ✅ DONE |
| 9 | Admin cannot mark completed | ✅ DONE |
| 10 | Admin UI flashes | ✅ DONE |
| 11 | Exit screens too fast | ✅ DONE |
| 12 | Confusing services (Dry, Express, Other) | ✅ DONE |
| 13 | No prices shown in service menu | ✅ DONE |
| 14 | Appointments don't show item details | ✅ DONE |
| 15 | int(input) crashes on invalid text | ✅ DONE |

---

## Fix Tasks (with Status)

### 1. utils.py - Fix get_washer_tasks() None issue
- **Status:** ✅ DONE
- Filter out None values before returning

### 2. customer_menu.py - Add date/time validation
- **Status:** ✅ DONE
- Validate YYYY-MM-DD format
- Validate HH:MM format

### 3. admin_menu.py - Add price calculation
- **Status:** ✅ DONE
- Add SERVICE_PRICES dict
- Calculate based on service_type and item_count

### 4. customer_menu.py - Add email validation
- **Status:** ✅ DONE
- Basic email format check (contains @ and .)

### 5. customer_menu.py - Fix email validation loop
- **Status:** ✅ DONE
- Loop allows retry instead of kicking user out
- Show helpful message with example

### 6. washer_menu.py - Fix task verification
- **Status:** ✅ DONE
- Verify task is actually assigned to washer's tasks list

### 7. customer_menu.py - Add cancel appointment
- **Status:** ✅ DONE
- Add option 4 in dashboard to cancel appointment

### 8. admin_menu.py - Add mark completed
- **Status:** ✅ DONE
- Add option to mark appointment as Completed

### 9. admin_menu.py - Add clear_screen/pause
- **Status:** ✅ DONE
- Add to: manage_customers, manage_appointments, manage_washers

### 10. main.py - Add pause before exit
- **Status:** ✅ DONE
- Add pause after each menu option

### 11. customer_menu.py + admin_menu.py - Hide password
- **Status:** ✅ DONE
- Password uses termios to hide input

### 12. Service types cleanup
- **Status:** ✅ DONE
- Removed: Dry Clean, Express Service, Other
- Services now: Wash (10 SR), Iron (5 SR), Wash & Iron (15 SR)

### 13. Show prices in menu
- **Status:** ✅ DONE
- Menu shows prices: "1. Wash - 10 SR"

### 14. Show item details in appointments
- **Status:** ✅ DONE
- Shows: "3 T-shirts, 2 Trousers" instead of just count