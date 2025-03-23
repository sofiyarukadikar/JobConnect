from app import create_app, db
from models.user import User, JobSeeker, Recruiter
# Import your Job model and any other models
from models.job import Job  # Adjust import path as needed

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created!")