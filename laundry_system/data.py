# Global data storage (in memory)
customers = []
appointments = []
tasks = []
staff = []

# ID counters
customer_id_counter = 1
appointment_id_counter = 1
task_id_counter = 1
staff_id_counter = 1


# Function to get next ID
def get_next_customer_id():
    global customer_id_counter
    customer_id_counter += 1
    return customer_id_counter - 1


def get_next_appointment_id():
    global appointment_id_counter
    appointment_id_counter += 1
    return appointment_id_counter - 1


def get_next_task_id():
    global task_id_counter
    task_id_counter += 1
    return task_id_counter - 1


def get_next_staff_id():
    global staff_id_counter
    staff_id_counter += 1
    return staff_id_counter - 1


PAYMENT_METHODS = {
    "1": "Credit Card",
    "2": "IBAN Transfer",
    "3": "STC Pay",
}

FAKE_PAYMENT_DETAILS = {
    "iban": "SA12 3456 7890 1234 5678 9012 34",
    "iban_bank": "Saudi National Bank (SNB)",
    "iban_holder": "Laundry Express Co.",
    "stc_pay": "+966 50 123 4567",
}

SERVICE_TYPES = {
    "1": "Wash",
    "2": "Iron",
    "3": "Wash & Iron",
}

SERVICE_PRICES = {
    "Wash": 10,
    "Iron": 5,
    "Wash & Iron": 15,
}
