import os
from flask import Flask, render_template, abort, request, has_request_context
from jinja2 import TemplateNotFound
from logger import get_logger

from loader import ABTestingLoader
from dtos.common.nav import get_main_menu
from dtos.common.footer import get_footer_menu
from dtos.homepage.homepage import get_main_topics, HeaderTopics

app = Flask(__name__)


@app.context_processor
def inject_global_variables():
    return dict(nav_menu=get_main_menu(), footer_menu=get_footer_menu())


logger = get_logger()

# Inject the custom loader
app.jinja_loader = ABTestingLoader(
    os.path.join(app.root_path, "templates_original"),
    os.path.join(app.root_path, "templates_final"),
)
app.jinja_env.cache = None


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


# NORMAL PATHS -> RENDERIZA LA PLANTILLA TRANSFORMADA A JINJA (templates_final)
@app.route("/")
def index():
    header_data: HeaderTopics = get_main_topics()
    return render_template(
        "index.html",
        main_topic=header_data.main_topic,
        topics=header_data.topics,
    )


@app.route("/<path:page_name>")
def catch_all(page_name):
    # Ignore the /migration/ path so it passes to the lower routes
    if page_name.startswith("migration/") or page_name == "migration":
        abort(404)

    if not page_name.endswith(".html"):
        abort(404)

    try:
        return render_template(page_name)
    except TemplateNotFound:
        abort(404)


# MIGRATION PATHS -> OLD DATA / PLANTILLA THEMEFOREST NO ADAPTADA (templates_original)
# NO SE SUBE A GIT.
@app.route("/migration")
@app.route("/migration/")
def migration_index():
    return render_template("index.html")


@app.route("/migration/<path:page_name>")
def migration_catch_all(page_name):
    if not page_name.endswith(".html"):
        abort(404)

    try:
        return render_template(page_name)
    except TemplateNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")