from datetime import datetime
import bcrypt
import logging
import random
import string

# Initialize logging
logging.basicConfig(
    filename='app.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def format_date(date_string, date_format="%Y-%m-%d"):
    """Parses and formats a date string."""
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return None

def generate_response(data=None, message=None, status_code=200):
    """Creates a standardized JSON response."""
    response = {"message": message, "data": data}
    return response, status_code

def hash_password(password):
    """Hashes a plaintext password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    """Checks if a plaintext password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_ticket_number(vehicle_id, year, month):
    """Generates a unique ticket number for a vehicle in a specific month."""
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{year}{month:02d}-{vehicle_id}-{unique_id}"

def log_error(message):
    """Logs an error message to the application log."""
    logging.error(message)

def log_info(message):
    """Logs an informational message to the application log."""
    logging.info(message)

def format_work_ticket(ticket, trips, drivers, authorizers):
    """Formats a work ticket for display or printing."""
    formatted_ticket = {
        "ticket_no": ticket.ticket_no,
        "vehicle_id": ticket.vehicle_id,
        "month": ticket.month,
        "year": ticket.year,
        "trips": [],
        "drivers": [driver.name for driver in drivers],
        "authorizers": [auth.name for auth in authorizers]
    }
    for trip in trips:
        formatted_ticket["trips"].append({
            "date": trip.date,
            "driver": trip.driver_id,
            "from": trip.from_location,
            "to": trip.to_location,
            "odometer_start": trip.odometer_start,
            "odometer_end": trip.odometer_end,
            "fuel_drawn": trip.fuel_drawn,
            "fuel_receipt_no": trip.fuel_receipt_no,
            "authorized_by": trip.authorized_by
        })
    return formatted_ticket
