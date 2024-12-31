#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from app import db
from sqlalchemy.orm import validates

#db = SQLAlchemy()
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'driver', 'authorizing_officer', 'transport_officer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    trips = db.relationship('Trip', foreign_keys='Trip.driver_id', backref='driver', lazy=True)
    authorized_trips = db.relationship('Trip', foreign_keys='Trip.authorized_by', backref='authorizer', lazy=True)

    def __repr__(self):
        return f"<User {self.username}, Role: {self.role}>"


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)  # Added field
    year = db.Column(db.Integer, nullable=False)      # Added field
    department = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    duty_station = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='active')  # Added field
    last_service_date = db.Column(db.Date, nullable=True)  # Added field
    next_service_due = db.Column(db.Date, nullable=True)   # Added field
    
    @validates('reg_no')
    def validate_reg_no(self, key, reg_no):
        if not reg_no or len(reg_no) < 4:
            raise ValueError("Registration number must be at least 4 characters")
        return reg_no

    @validates('year')
    def validate_year(self, key, year):
        current_year = datetime.now().year
        if not (1900 <= year <= current_year):
            raise ValueError(f"Year must be between 1900 and {current_year}")
        return year

    # Relationships
    trips = db.relationship('Trip', backref='vehicle', lazy=True)
    work_tickets = db.relationship('WorkTicket', backref='vehicle', lazy=True)

    def __repr__(self):
        return f"<Vehicle {self.reg_no}, Make: {self.make}>"


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    odometer_start = db.Column(db.Integer, nullable=False)
    odometer_end = db.Column(db.Integer, nullable=True)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    fuel_drawn = db.Column(db.Float, nullable=True)
    fuel_receipt_no = db.Column(db.String(50), nullable=True)
    time_out = db.Column(db.Time, nullable=False)
    time_in = db.Column(db.Time, nullable=True)
    authorized_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    authorization_status = db.Column(db.String(20), default="Pending")  # 'Pending', 'Approved', 'Rejected'

    def __repr__(self):
        return f"<Trip Driver: {self.driver_id}, Vehicle: {self.vehicle_id}, Date: {self.date}>"


class WorkTicket(db.Model):
    __tablename__ = 'work_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_no = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    details = db.Column(db.JSON, nullable=False)  # JSON with trips and authorization details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WorkTicket {self.ticket_no}, Vehicle ID: {self.vehicle_id}, Date: {self.month}/{self.year}>"
