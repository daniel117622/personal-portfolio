import traceback

from flask import jsonify, render_template, request
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
        
        # Extract the raw traceback
        tb = error.__traceback__
        tb_info = traceback.extract_tb(tb)
        
        # Identify the exact point of failure (the last frame in the stack)
        last_frame = tb_info[-1] if tb_info else None
        
        # Build a readable, structured call stack
        call_stack = [
            {
                "file": frame.filename,
                "line_no": frame.lineno,
                "function": frame.name,
                "code": frame.line
            }
            for frame in tb_info
        ]

        # Construct the detailed JSON payload
        error_payload = {
            "error_type": type(error).__name__,
            "message": str(error),
            "failed_at": {
                "file": last_frame.filename if last_frame else None,
                "line_no": last_frame.lineno if last_frame else None,
            },
            "request": {
                "method": request.method,
                "url": request.url,
            },
            "call_stack": call_stack
        }

        # Return as a JSON response with a 500 status code
        return jsonify(error_payload), 500