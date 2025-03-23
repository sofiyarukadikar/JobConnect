import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from extensions import db
from datetime import datetime

class JobPosting(db.Model):
    """Model for job postings."""
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract, etc.
    experience_level = db.Column(db.String(50))  # Entry, Mid, Senior
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Foreign Keys
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False)
    
    # Relationships
    applications = db.relationship('JobApplication', backref='job_posting', lazy=True)
    
    def __repr__(self):
        return f'<JobPosting {self.title} at {self.company}>'


class JobApplication(db.Model):
    """Model for job applications."""
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, interviewed, offered, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('job_seekers.id'), nullable=False)
    
    def __repr__(self):
        return f'<JobApplication {self.id} for job {self.job_posting_id}>'


# For compatibility with existing code that imports 'Job'
# We'll create an alias to JobPosting
Job = JobPosting
