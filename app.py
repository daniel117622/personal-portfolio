import os
from flask import Flask

from loader import ABTestingLoader
from logger import get_logger
from context import inject_global_variables
from errors import register_error_handlers
from routes import register_blueprints

logger = get_logger()


def create_app() -> Flask:
    app = Flask(__name__)

    app.jinja_loader = ABTestingLoader(
        os.path.join(app.root_path, "templates_original"),
        os.path.join(app.root_path, "templates_final"),
    )
    app.jinja_env.cache = None

    app.context_processor(inject_global_variables)
    register_error_handlers(app, logger)
    register_blueprints(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")