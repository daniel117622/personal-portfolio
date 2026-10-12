import os
from flask import Flask

from loader import ABTestingLoader
from logger import get_logger
from context import inject_global_variables
from errors import register_error_handlers
from routes import register_blueprints

from realtime.bus import bus

from config import Config

logger = get_logger(__name__)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates_final")

    
    app.jinja_loader = ABTestingLoader(
        os.path.join(app.root_path, "templates_original"),
        os.path.join(app.root_path, "templates_final"),
    )
    app.jinja_env.cache = None

    app.context_processor(inject_global_variables)


    register_error_handlers(app, logger)
    register_blueprints(app)

    # Hook the realtime handlers (SOCKET.IO)
    bus.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    bus.socketio.run(app, debug=True, port=8000, host="0.0.0.0")