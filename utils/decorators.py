from functools import wraps
from flask import redirect, url_for, flash, current_app
from flask_login import current_user
from datetime import datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value  # Return as-is if it's not a datetime object

def jobseeker_required(f):
    """
    Decorator to restrict access to job seeker users only.
    Redirects to login page if user is not logged in.
    Redirects to home page with a message if user is not a job seeker.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if current_user.user_type != 'job_seeker':
            flash('Access denied. This area is only for job seekers.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function

def recruiter_required(f):
    """
    Decorator to restrict access to recruiter users only.
    Redirects to login page if user is not logged in.
    Redirects to home page with a message if user is not a recruiter.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if current_user.user_type != 'recruiter':
            flash('Access denied. This area is only for recruiters.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function