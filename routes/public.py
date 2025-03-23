from flask import Blueprint, render_template, redirect, url_for
from models.job import Job

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    # Get featured jobs for the homepage
    featured_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    return render_template('public/index.html', featured_jobs=featured_jobs)

@public_bp.route('/about')
def about():
    return render_template('public/about.html')
@public_bp.route('/browse-categories')
def browse_categories():
    # Your logic here
    return render_template('public/browse_categories.html')
@public_bp.route('/faq')
def faq():
    return render_template('public/faq.html')

@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')

@public_bp.route('/browse-jobs')
def browse_jobs():
    # Redirect to job search page with no filters
    return redirect(url_for('jobseeker.job_search'))


@public_bp.route('/subscribe', methods=['POST'])
def subscribe_newsletter():
    # Handle newsletter subscription logic here
    email = request.form.get('email')
    if email:
        # Save to database or send confirmation email
        flash("Successfully subscribed to the newsletter!", "success")
    else:
        flash("Please enter a valid email address.", "danger")
    return redirect(url_for('public.index'))


@public_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('public/privacy_policy.html')
