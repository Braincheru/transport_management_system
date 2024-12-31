from flask import Blueprint
from app.routes.auth import bp as auth_bp
from app.routes.driver import bp as driver_bp
from app.routes.officer import bp as officer_bp
from app.routes.transport_officer import bp as transport_officer_bp

def register_routes(app):
    """Registers all route blueprints with the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(driver_bp)
    app.register_blueprint(officer_bp)
    app.register_blueprint(transport_officer_bp)
