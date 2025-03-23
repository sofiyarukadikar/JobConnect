import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or '00fd89c58ed7d411b04fe3a8d01743c6'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jobconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login settings
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload