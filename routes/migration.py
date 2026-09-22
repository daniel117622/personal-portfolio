from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

migration_bp = Blueprint("migration", __name__, url_prefix="/migration")


@migration_bp.route("")
@migration_bp.route("/")
def migration_index():
    return render_template("index.html")


@migration_bp.route("/<path:page_name>")
def migration_catch_all(page_name):
    if not page_name.endswith(".html"):
        abort(404)

    try:
        return render_template(page_name)
    except TemplateNotFound:
        abort(404)