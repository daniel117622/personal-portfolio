from flask import render_template, request
from jinja2 import TemplateNotFound


def register_error_handlers(app, logger):
    @app.errorhandler(404)
    def page_not_found(error):
        logger.warning(f"404 Not Found: {request.path}")
        try:
            return render_template("404.html"), 404
        except TemplateNotFound:
            return "404 - Page Not Found", 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Server Error: {error}", exc_info=True)
        return "500 - Internal Server Error", 500