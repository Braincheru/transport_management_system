import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'jicheaaaaaa1232')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///transport.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jicheaaaaaa1232')
