from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models.user import User, JobSeeker, Recruiter
from extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register-choice', methods=['GET'])
def register_choice():
    if current_user.is_authenticated:
        return redirect(url_for('jobseeker.dashboard' if current_user.user_type == 'job_seeker' else 'recruiter.dashboard'))
    return render_template('auth/register_choice.html')

@auth_bp.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    if current_user.is_authenticated:
        return redirect(url_for('jobseeker.dashboard' if current_user.user_type == 'job_seeker' else 'recruiter.dashboard'))
    
    if user_type not in ['jobseeker', 'recruiter']:
        flash('Invalid user type', 'danger')
        return redirect(url_for('auth.register_choice'))
    
    if request.method == 'POST':
        # Process registration form
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('auth/register.html', user_type=user_type)
        
        # Generate a username from email (before the @ symbol)
        username = email.split('@')[0]

        # Check if username exists and append numbers if needed
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        # Create appropriate user type
        if user_type == 'jobseeker':
            new_user = JobSeeker(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
        else:  # recruiter
            company = request.form.get('company')
            new_user = Recruiter(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                company_name=company  # Note: changed from company to company_name to match model
            )
        
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', user_type=user_type)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('jobseeker.dashboard' if current_user.user_type == 'job_seeker' else 'recruiter.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                if user.user_type == 'job_seeker':
                    next_page = url_for('jobseeker.dashboard')
                else:
                    next_page = url_for('recruiter.dashboard')
            return redirect(next_page)
        
        flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('public.index'))
