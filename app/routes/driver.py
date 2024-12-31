from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Trip
from app import db
from flask import jsonify
from app.services.logger import logger_service
bp = Blueprint('driver', __name__, url_prefix='/driver')

from app.middleware import role_required
from app.services.trip import TripService

trip_service = TripService()

@bp.route('/dashboard')
@login_required
@role_required('driver')
def dashboard():
    with open('app/static/dashboard.jsx', 'r') as f:
        react_code = f.read()
    return render_template('driver_dashboard.html', react_code=react_code)

@bp.route('/create_trip', methods=['POST'])
@login_required
@role_required('driver')
def create_trip():
    try:
        trip_data = request.get_json()
        new_trip = trip_service.create_trip(
            driver_id=current_user.id,
            vehicle_id=trip_data['vehicle_id'],
            **trip_data
        )
        return jsonify({
            'message': 'Trip created successfully',
            'trip_id': new_trip.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger_service.logger.error(f"Error creating trip: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500