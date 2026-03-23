# Global data storage (in memory)
customers = []
appointments = []
tasks = []
washers = []

# ID counters
customer_id_counter = 1
appointment_id_counter = 1
task_id_counter = 1
washer_id_counter = 1


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


def get_next_washer_id():
    global washer_id_counter
    washer_id_counter += 1
    return washer_id_counter - 1
