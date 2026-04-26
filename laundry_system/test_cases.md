# Laundry System - Test Cases

---

## TC-01: Customer Registration, Login, Booking & Tracking
**Objective:** Verify customer workflow - register, login, book service, track status. (FR-1, FR-2, FR-3)

**Scenario:**
1. Register: name "John", email "john@test.com", password "pass123"
2. Login: email + password
3. Book: date "2026-05-01", time "10:00", service "Wash & Iron", 5 items, payment "Cash"
4. Track: View appointments

**The system shall:**
- Create appointment with "Pending" status
- Calculate price 75 SR correctly
- Display booking with correct date/time/status

---

## TC-02: Washer View Tasks & Update Status  
**Objective:** Verify washer can view assigned tasks and update status with notes. (FR-7, FR-8, FR-9)

**Preconditions:**
- Washer A must have at least 1 task assigned
- Washer B must have a different task assigned
- Washer A is logged in

**Scenario:**
1. Login: Washer A
2. View tasks - only shows A's task, NOT B's
3. Update status to "Done"
4. Add note "Completed"

**The system shall:**
- Update task status to "Done"
- Save the note
- Allow customer to view the notes

---

## TC-03: Admin Manage, Assign & Reports
**Objective:** Verify admin can manage customers/washers, assign work, view reports. (FR-11, FR-13, FR-14, FR-15)

**Preconditions:**
- At least 1 customer must exist
- At least 1 washer must exist
- Admin must be logged in

**Scenario:**
1. View customers, delete one
2. Add washer
3. Assign task to washer
4. View reports

**The system shall:**
- Delete selected customer
- Create washer with unique ID
- Link task to washer
- Display accurate report statistics

---

## TC-04: End to End Lifecycle
**Objective:** Full workflow: customer book → admin assign → washer complete → customer view. (All FRs)

**Scenario:**
1. Customer: register → book (Pending)
2. Admin: assign task (In Progress)
3. Washer: view → update status (Done) → add note
4. Customer: view final status

**The system shall:**
- Display "Done" status to customer
- Show washer note "Completed"

---

## Summary

| Test | FRs |
|------|-----|
| TC-01 | FR1-FR3 |
| TC-02 | FR7-FR9 |
| TC-03 | FR11, FR13-FR15 |
| TC-04 | All |