from routes.main import main_bp
from routes.migration import migration_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(migration_bp)