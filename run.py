from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app import db
from app.routes import register_routes

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
with app.app_context():
    register_routes(app)
    db.create_all()  # Create database tables

@app.route('/')
def index():
    return "Transport Management System API"

if __name__ == '__main__':
    app.run(debug=True)
