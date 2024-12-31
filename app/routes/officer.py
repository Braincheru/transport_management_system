from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Trip
from app import db

bp = Blueprint('officer', __name__, url_prefix='/officer')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'officer':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.dashboard'))
    pending_trips = Trip.query.filter_by(authorized=False).all()
    return render_template('officer_dashboard.html', pending_trips=pending_trips)

@bp.route('/authorize_trip/<int:trip_id>', methods=['POST'])
@login_required
def authorize_trip(trip_id):
    if current_user.role != 'officer':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('auth.dashboard'))

    trip = Trip.query.get(trip_id)
    if not trip:
        flash('Trip not found!', 'danger')
        return redirect(url_for('officer.dashboard'))

    trip.authorized = True
    db.session.commit()
    flash('Trip authorized successfully.', 'success')
    return redirect(url_for('officer.dashboard'))
