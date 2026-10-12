from routes.main import main_bp
from routes.migration import migration_bp
from routes.calendar_demo import calendar_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(migration_bp)
    app.register_blueprint(calendar_bp)