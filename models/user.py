from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from extensions import db

class User(db.Model, UserMixin):
    """Base user model with common attributes and methods."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class JobSeeker(User):
    """Job seeker specific model."""
    __tablename__ = 'job_seekers'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)  # Stored as comma-separated values
    experience_years = db.Column(db.Integer, nullable=True)
    resume_url = db.Column(db.String(255), nullable=True)
    
    # Relationships
    applications = db.relationship('JobApplication', backref='applicant', lazy=True)
    profile = db.relationship('Profile', backref='job_seeker', uselist=False, lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'job_seeker',
    }
    
    def __repr__(self):
        return f'<JobSeeker {self.first_name} {self.last_name}>'


class Recruiter(User):
    """Recruiter specific model."""
    __tablename__ = 'recruiters'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(50), nullable=True)
    company_size = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    
    # Relationships
    job_postings = db.relationship('JobPosting', backref='recruiter', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'recruiter',
    }
    
    def __repr__(self):
        return f'<Recruiter {self.company_name}>'
