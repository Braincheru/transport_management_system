from datetime import datetime, timedelta
from app.models import Trip, Vehicle
from app.services.logger import logger_service
from app import db

class TripService:
    @logger_service.log_action('Trip Creation')
    def create_trip(self, driver_id, vehicle_id, **trip_data):
        # Check if vehicle is available
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle or vehicle.status != 'active':
            raise ValueError("Vehicle is not available")
            
        # Check for overlapping trips
        existing_trip = Trip.query.filter(
            Trip.vehicle_id == vehicle_id,
            Trip.date == trip_data['date'],
            Trip.time_in.is_(None)
        ).first()
        
        if existing_trip:
            raise ValueError("Vehicle already has an active trip")
            
        # Create new trip with validation
        new_trip = Trip(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            date=trip_data['date'],
            from_location=trip_data['from_location'],
            to_location=trip_data['to_location'],
            odometer_start=trip_data['odometer_start'],
            time_out=datetime.now()
        )
        
        db.session.add(new_trip)
        db.session.commit()
        return new_trip

    @logger_service.log_action('Trip Completion')
    def complete_trip(self, trip_id, odometer_end, fuel_drawn=None):
        trip = Trip.query.get(trip_id)
        if not trip:
            raise ValueError("Trip not found")
            
        if trip.time_in:
            raise ValueError("Trip already completed")
            
        if odometer_end <= trip.odometer_start:
            raise ValueError("End odometer reading must be greater than start reading")
            
        trip.odometer_end = odometer_end
        trip.time_in = datetime.now()
        trip.fuel_drawn = fuel_drawn
        
        db.session.commit()
        return trip