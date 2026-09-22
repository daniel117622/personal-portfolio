from typing import List

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from repository import repos
from dtos.homepage import HeaderTopics, SocialActivity
from dtos.devlogs import DevBlogSummary
from dtos.articles import ArticleSummary

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    header_data: HeaderTopics = repos.homepage.get_main_topics()
    devlogs: List[DevBlogSummary] = repos.devlogs.get_devlogs()
    articles: List[ArticleSummary] = repos.articles.get_articles_summary()
    socials: SocialActivity = repos.homepage.get_social_activity()

    return render_template(
        "index.html",
        main_topic=header_data.main_topic,
        topics=header_data.topics,
        devlogs=devlogs,
        articles=articles,
        socials=socials,
    )


@main_bp.route("/article")
def article_by_id():
    article_id = request.args.get("id", type=int)
    article_content = repos.articles.get_article_by_id(article_id)

    return render_template("article_read.html", article=article_content)


@main_bp.route("/<path:page_name>")
def catch_all(page_name):
    # Guard: migration paths are owned by migration_bp
    if page_name == "migration" or page_name.startswith("migration/"):
        abort(404)

    if not page_name.endswith(".html"):
        abort(404)

    try:
        return render_template(page_name)
    except TemplateNotFound:
        abort(404)