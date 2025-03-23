from flask import Blueprint

# Import all blueprints
from .auth import auth_bp
from .jobseeker import jobseeker_bp
from .recruiter import recruiter_bp
from .public import public_bp

# List of all blueprints to register
blueprints = [auth_bp, jobseeker_bp, recruiter_bp, public_bp]
