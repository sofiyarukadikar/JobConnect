# Import all models to make them available when importing from models
from models.user import User, JobSeeker, Recruiter
from models.job import JobPosting, JobApplication, Job
from models.profile import Profile
from models.resume import Resume

# This ensures all models are available when importing from models package
__all__ = [
    'User', 
    'JobSeeker', 
    'Recruiter', 
    'JobPosting', 
    'JobApplication', 
    'Job',
    'Profile',
    'Resume'
]