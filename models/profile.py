from extensions import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('job_seekers.id'), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    summary = db.Column(db.Text)
    skills = db.Column(db.Text)  # Comma-separated skills
    experience_years = db.Column(db.Integer)
    linkedin_url = db.Column(db.String(200))
    portfolio_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Profile for JobSeeker {self.job_seeker_id}>'
    
    def get_skills_list(self):
        """Return skills as a list"""
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(',')]
