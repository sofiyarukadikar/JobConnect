from datetime import datetime
from extensions import db

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('job_seekers.id'), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with JobSeeker
    job_seeker = db.relationship('JobSeeker', backref='resumes')
    
    def __repr__(self):
        return f'<Resume {self.id}: {self.title}>'
