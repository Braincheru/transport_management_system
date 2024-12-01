from app.models import db, Trip
from app.utils import log_error, log_info

def create_trip(driver_id, vehicle_id, date, from_location, to_location, odometer_start, time_out, authorizing_officer):
    """Creates a new trip."""
    try:
        trip = Trip(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            date=date,
            from_location=from_location,
            to_location=to_location,
            odometer_start=odometer_start,
            time_out=time_out,
            authorized_by=authorizing_officer
        )
        db.session.add(trip)
        db.session.commit()
        log_info(f"Trip created successfully: {trip}")
        return trip
    except Exception as e:
        log_error(f"Error creating trip: {str(e)}")
        return None

def update_trip_end(trip_id, odometer_end, time_in, fuel_drawn, fuel_receipt_no):
    """Updates the end details of a trip."""
    try:
        trip = Trip.query.get(trip_id)
        if trip:
            trip.odometer_end = odometer_end
            trip.time_in = time_in
            trip.fuel_drawn = fuel_drawn
            trip.fuel_receipt_no = fuel_receipt_no
            db.session.commit()
            log_info(f"Trip updated successfully: {trip}")
            return trip
        return None
    except Exception as e:
        log_error(f"Error updating trip: {str(e)}")
        return None
