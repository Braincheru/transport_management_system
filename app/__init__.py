from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'


    from app.routes import driver, officer, transport_officer, auth
    app.register_blueprint(driver.bp)
    app.register_blueprint(officer.bp)
    app.register_blueprint(transport_officer.bp)
    app.register_blueprint(auth.bp)

    return app
