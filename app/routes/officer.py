'''from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Trip, db

bp = Blueprint('officer', __name__, url_prefix='/officer')

@bp.route('/authorize_trip/<int:trip_id>', methods=['POST'])
@jwt_required()
def authorize_trip(trip_id):
    data = request.json
    trip = Trip.query.get_or_404(trip_id)
    trip.authorization_status = 'Approved' if data.get('approve') else 'Rejected'
    trip.authorized_by = get_jwt_identity()['id']
    db.session.commit()

    return jsonify({'message': 'Trip updated successfully'}), 200
'''

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
