from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.job import Job, JobApplication
from models.profile import Profile
from models.resume import Resume
from extensions import db
import os
from werkzeug.utils import secure_filename
from utils.decorators import jobseeker_required

jobseeker_bp = Blueprint('jobseeker', __name__, url_prefix='/jobseeker')

@jobseeker_bp.route('/dashboard')
@login_required
@jobseeker_required
def dashboard():
    # Get recent job applications
    recent_applications = JobApplication.query.filter_by(applicant_id=current_user.id).order_by(JobApplication.applied_at.desc()).limit(5).all()
    
    # Get recommended jobs based on user profile
    recommended_jobs = Job.query.filter_by(is_active=True).limit(10).all()  # Placeholder - would need more logic
    
    return render_template('jobseeker/dashboard.html', applications=recent_applications, jobs=recommended_jobs)

@jobseeker_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@jobseeker_required
def profile():
    if request.method == 'POST':
        # Update profile information
        profile = current_user.profile or Profile(job_seeker_id=current_user.id)
        
        profile.phone = request.form.get('phone')
        profile.location = request.form.get('location')
        profile.summary = request.form.get('summary')
        profile.skills = request.form.get('skills')
        profile.experience_years = request.form.get('experience_years')
        
        if not current_user.profile:
            db.session.add(profile)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('jobseeker.profile'))
    
    return render_template('jobseeker/profile.html')

@jobseeker_bp.route('/resumes')
@login_required
@jobseeker_required
def resumes():
    user_resumes = Resume.query.filter_by(job_seeker_id=current_user.id).all()
    return render_template('jobseeker/resumes.html', resumes=user_resumes)

@jobseeker_bp.route('/resume-builder', methods=['GET', 'POST'])
@login_required
@jobseeker_required
def resume_builder():
    if request.method == 'POST':
        # Process resume builder form
        title = request.form.get('title')
        content = request.form.get('content')  # JSON or HTML representation of resume
        
        new_resume = Resume(
            job_seeker_id=current_user.id,
            title=title,
            file_url=content  # Assuming content is the file URL or path
        )
        db.session.add(new_resume)
        db.session.commit()
        
        flash('Resume created successfully', 'success')
        return redirect(url_for('jobseeker.resumes'))
    
    return render_template('jobseeker/resume_builder.html')

@jobseeker_bp.route('/job-search')
@login_required
@jobseeker_required
def job_search():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    category = request.args.get('category', '')
    
    # Build search query
    jobs_query = Job.query.filter_by(is_active=True)
    
    if query:
        jobs_query = jobs_query.filter(Job.title.contains(query) | Job.description.contains(query))
    
    if location:
        jobs_query = jobs_query.filter(Job.location.contains(location))
    
    if category:
        jobs_query = jobs_query.filter(Job.category == category)
    
    jobs = jobs_query.order_by(Job.created_at.desc()).all()
    
    return render_template('jobseeker/job_search.html', jobs=jobs, query=query, location=location, category=category)

@jobseeker_bp.route('/applications')
@login_required
@jobseeker_required
def applications():
    user_applications = JobApplication.query.filter_by(applicant_id=current_user.id).order_by(JobApplication.applied_at.desc()).all()
    return render_template('jobseeker/applications.html', applications=user_applications)

@jobseeker_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
@jobseeker_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing_application = JobApplication.query.filter_by(job_posting_id=job_id, applicant_id=current_user.id).first()
    if existing_application:
        flash('You have already applied for this job', 'warning')
        return redirect(url_for('jobseeker.job_search'))

    if request.method == 'POST':
        resume_id = request.form.get('resume_id')
        cover_letter = request.form.get('cover_letter', '')

        new_application = JobApplication(
            job_posting_id=job_id,
            applicant_id=current_user.id,
            resume_url=resume_id,  # Note: This might need adjustment based on how resume URLs are stored
            cover_letter=cover_letter,
            status='pending'
        )
        db.session.add(new_application)
        db.session.commit()
        
        flash('Application submitted successfully', 'success')
        return redirect(url_for('jobseeker.applications'))
    
    # Get user's resumes for selection
    user_resumes = Resume.query.filter_by(job_seeker_id=current_user.id).all()
    
    return render_template('jobseeker/apply.html', job=job, resumes=user_resumes)
