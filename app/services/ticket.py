from app.models import db, WorkTicket, Trip
from app.utils import generate_ticket_number, log_error

def create_ticket(vehicle_id, year, month):
    """Creates a work ticket for a specific vehicle and month."""
    try:
        # Fetch trips for the vehicle in the given month
        trips = Trip.query.filter(
            Trip.vehicle_id == vehicle_id,
            Trip.date.between(f"{year}-{month}-01", f"{year}-{month}-31")
        ).all()

        # Generate ticket number
        ticket_no = generate_ticket_number(vehicle_id, year, month)

        # Consolidate details
        details = f"Work Ticket for Vehicle {vehicle_id} in {month}/{year}"
        ticket = WorkTicket(
            ticket_no=ticket_no,
            vehicle_id=vehicle_id,
            month=str(month).zfill(2),
            year=str(year),
            details=details
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket
    except Exception as e:
        log_error(f"Error creating ticket: {str(e)}")
        return None

def get_tickets_by_vehicle(vehicle_id):
    """Retrieves all tickets for a specific vehicle."""
    return WorkTicket.query.filter_by(vehicle_id=vehicle_id).all()
