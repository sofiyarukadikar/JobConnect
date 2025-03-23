from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.job import Job, JobApplication
from utils.decorators import recruiter_required
from extensions import db

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/dashboard')
@login_required
@recruiter_required
def dashboard():
    # Get active job listings
    active_jobs = Job.query.filter_by(recruiter_id=current_user.id, is_active=True).order_by(Job.created_at.desc()).all()
    
    # Get recent applications
    recent_applications = JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id).order_by(JobApplication.applied_at.desc()).limit(10).all()

    # Get application statistics
    application_stats = {
        'total': JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id).count(),
        'new': JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id, JobApplication.status == 'pending').count(),
        'reviewing': JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id, JobApplication.status == 'reviewed').count(),
        'interviewed': JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id, JobApplication.status == 'interviewed').count()
    }
    
    return render_template('recruiter/dashboard.html', 
                          active_jobs=active_jobs, 
                          recent_applications=recent_applications, 
                          stats=application_stats)

@recruiter_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
@recruiter_required
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        category = request.form.get('category')
        job_type = request.form.get('job_type')
        salary_min = request.form.get('salary_min')
        salary_max = request.form.get('salary_max')
        requirements = request.form.get('requirements')
        
        new_job = Job(
            recruiter_id=current_user.id,
            title=title,
            description=description,
            location=location,
            category=category,
            job_type=job_type,
            salary_min=salary_min,
            salary_max=salary_max,
            requirements=requirements,
            is_active=True
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job posted successfully', 'success')
        return redirect(url_for('recruiter.manage_jobs'))
    
    return render_template('recruiter/post_job.html')

@recruiter_bp.route('/manage-jobs')
@login_required
@recruiter_required
def manage_jobs():
    jobs = Job.query.filter_by(recruiter_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('recruiter/manage_jobs.html', jobs=jobs)

@recruiter_bp.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
@recruiter_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Ensure the job belongs to the current recruiter
    if job.recruiter_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('recruiter.manage_jobs'))
    
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.location = request.form.get('location')
        job.category = request.form.get('category')
        job.job_type = request.form.get('job_type')
        job.salary_min = request.form.get('salary_min')
        job.salary_max = request.form.get('salary_max')
        job.requirements = request.form.get('requirements')
        job.is_active = 'active' in request.form
        
        db.session.commit()
        flash('Job updated successfully', 'success')
        return redirect(url_for('recruiter.manage_jobs'))
    
    return render_template('recruiter/edit_job.html', job=job)

@recruiter_bp.route('/applications')
@login_required
@recruiter_required
def applications():
    # Filter by job_id if provided
    job_id = request.args.get('job_id')
    
    if job_id:
        # Ensure the job belongs to the current recruiter
        job = Job.query.get_or_404(job_id)
        if job.recruiter_id != current_user.id:
            flash('Access denied', 'danger')
            return redirect(url_for('recruiter.dashboard'))
        
        applications = JobApplication.query.filter_by(job_posting_id=job_id).order_by(JobApplication.applied_at.desc()).all()
        return render_template('recruiter/applications.html', applications=applications, job=job)

    # Show all applications for all jobs
    applications = JobApplication.query.join(Job).filter(Job.recruiter_id == current_user.id).order_by(JobApplication.applied_at.desc()).all()
    return render_template('recruiter/applications.html', applications=applications, job=None)

@recruiter_bp.route('/update-application-status/<int:app_id>', methods=['POST'])
@login_required
@recruiter_required
def update_application_status(app_id):
    application = JobApplication.query.get_or_404(app_id)

    # Ensure the application's job belongs to the current recruiter
    if application.job_posting.recruiter_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('recruiter.applications'))

    new_status = request.form.get('status')
    if new_status in ['pending', 'reviewed', 'interviewed', 'offered', 'rejected']:
        application.status = new_status
        db.session.commit()
        flash('Application status updated', 'success')
    else:
        flash('Invalid status', 'danger')

    return redirect(url_for('recruiter.applications', job_id=application.job_posting_id))
