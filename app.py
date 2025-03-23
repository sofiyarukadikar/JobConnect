from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from datetime import datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Register the custom Jinja2 filter
    app.jinja_env.filters['datetime'] = datetimeformat

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.jobseeker import jobseeker_bp
    from routes.recruiter import recruiter_bp
    from routes.public import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobseeker_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(public_bp)

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

    return app

app = create_app()

# Custom datetime filter
@app.template_filter('datetime')
def format_datetime(value):
    if value is None:
        return "N/A"
    return value.strftime("%Y-%m-%d %H:%M")

if __name__ == '__main__':
    app.run(debug=True)
