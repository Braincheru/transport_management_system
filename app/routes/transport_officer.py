from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import extract
from datetime import datetime
import json

from app.models import Trip, WorkTicket, db
from app.services.ticket import create_ticket, get_tickets_by_vehicle

bp = Blueprint('transport_officer', __name__, url_prefix='/transport_officer')


@bp.route('/dashboard')
@login_required
def dashboard():
    """Render the transport officer's dashboard."""
    if current_user.role != 'transport_officer':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.dashboard'))

    tickets = WorkTicket.query.all()
    return render_template('transport_officer_dashboard.html', tickets=tickets)


@bp.route('/generate_work_ticket', methods=['POST'])
@login_required
def generate_work_ticket():
    """Generate a work ticket for approved trips."""
    if current_user.role != 'transport_officer':
        return jsonify({'message': 'Unauthorized action'}), 403

    data = request.json
    vehicle_id = data.get('vehicle_id')
    month = data.get('month')
    year = data.get('year')

    # Validate input
    if not vehicle_id or not month or not year:
        return jsonify({'message': 'Vehicle ID, month, and year are required'}), 400

    # Fetch approved trips for the specified vehicle, month, and year
    trips = Trip.query.filter(
        Trip.vehicle_id == vehicle_id,
        extract('month', Trip.date) == int(month),
        extract('year', Trip.date) == int(year),
        Trip.authorization_status == 'Approved'
    ).all()

    if not trips:
        return jsonify({'message': 'No approved trips found for this vehicle in the specified month'}), 404

    # Generate the ticket number
    existing_tickets = WorkTicket.query.filter_by(vehicle_id=vehicle_id, month=month, year=year).count()
    ticket_no = f"{year}-{str(month).zfill(2)}-{existing_tickets + 1}"

    # Prepare work ticket details
    driver_list = {trip.driver_id: f"Driver {trip.driver_id}" for trip in trips}  # Example names
    authorizer_list = {trip.authorized_by: f"Officer {trip.authorized_by}" for trip in trips}

    details = {
        "drivers": list(driver_list.values()),
        "authorizers": list(authorizer_list.values()),
        "trips": [
            {
                "date": trip.date.strftime("%Y-%m-%d"),
                "driver_no": list(driver_list.keys()).index(trip.driver_id) + 1,
                "from_to": f"{trip.from_location} - {trip.to_location}",
                "authorizer_no": list(authorizer_list.keys()).index(trip.authorized_by) + 1,
                "fuel_drawn": trip.fuel_drawn or 0,
                "fuel_receipt": trip.fuel_receipt_no or "N/A",
                "time_out": trip.time_out.strftime("%H:%M"),
                "time_in": trip.time_in.strftime("%H:%M") if trip.time_in else "N/A",
                "odometer_start": trip.odometer_start,
                "odometer_end": trip.odometer_end or 0,
                "distance": (trip.odometer_end or 0) - trip.odometer_start
            } for trip in trips
        ]
    }

    # Create and save the work ticket
    work_ticket = WorkTicket(
        ticket_no=ticket_no,
        vehicle_id=vehicle_id,
        month=month,
        year=year,
        details=json.dumps(details)
    )
    db.session.add(work_ticket)
    db.session.commit()

    return jsonify({'message': 'Work ticket generated successfully', 'ticket_no': ticket_no}), 201


@bp.route('/work_tickets', methods=['GET'])
@login_required
def get_all_work_tickets():
    """Fetch all work tickets."""
    if current_user.role not in ['transport_officer', 'officer']:
        return jsonify({'message': 'Unauthorized access'}), 403

    work_tickets = WorkTicket.query.all()
    result = [
        {
            "ticket_no": ticket.ticket_no,
            "vehicle_id": ticket.vehicle_id,
            "month": ticket.month,
            "year": ticket.year,
            "details": json.loads(ticket.details),
            "created_at": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for ticket in work_tickets
    ]
    return jsonify(result), 200


@bp.route('/tickets/<vehicle_id>', methods=['GET'])
@login_required
def get_tickets(vehicle_id):
    """Fetch all tickets for a specific vehicle."""
    if current_user.role not in ['transport_officer', 'officer']:
        return jsonify({'message': 'Unauthorized access'}), 403

    tickets = get_tickets_by_vehicle(vehicle_id)
    return jsonify({"tickets": [ticket.serialize() for ticket in tickets]}), 200
