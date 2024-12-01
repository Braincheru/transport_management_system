from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Trip
from app import db

bp = Blueprint('driver', __name__, url_prefix='/driver')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'driver':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.dashboard'))
    trips = Trip.query.filter_by(driver_id=current_user.id).all()
    return render_template('driver_dashboard.html', trips=trips)

@bp.route('/create_trip', methods=['POST'])
@login_required
def create_trip():
    if current_user.role != 'driver':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.dashboard'))

    data = request.form
    new_trip = Trip(
        driver_id=current_user.id,
        vehicle_id=data['vehicle_id'],
        date=data['trip_date'],
        from_location=data['from_location'],
        to_location=data['to_location'],
        odometer_start=data['odometer_start']
    )
    db.session.add(new_trip)
    db.session.commit()
    flash('Trip created successfully.', 'success')
    return redirect(url_for('driver.dashboard'))
