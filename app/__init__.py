from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from app.services.logger import LoggerService

db = SQLAlchemy()
#migrate = Migrate()
login_manager = LoginManager()
#login_manager.login_view = 'auth.login'
logger_service = LoggerService()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    #migrate.init_app(app, db)
    login_manager.init_app(app)
    print(f"LoginManager initialized: {login_manager}")
    

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'


    from app.routes import auth, driver, officer, transport_officer    
    app.register_blueprint(auth.bp)
    app.register_blueprint(driver.bp)
    app.register_blueprint(transport_officer.bp)
    app.register_blueprint(officer.bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
