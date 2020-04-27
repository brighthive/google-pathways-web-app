from flask import Blueprint, render_template

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import PathwaysProgram

config = ConfigurationFactory.from_env()
static_blueprint = Blueprint("static", __name__)


@static_blueprint.route("/sitemap.xml", methods=["GET"])
def site_map():
    pathways_programs = PathwaysProgram.query.order_by(
        PathwaysProgram.updated_at.desc()
    )

    return render_template(
        "sitemap.xml", pathways_programs=pathways_programs, base_url=config.BASE_URL
    )


@static_blueprint.route("/robots.txt", methods=["GET"])
def robots():
    """Returns a https://support.google.com/webmasters/answer/6062596?hl=en."""
    return f"Sitemap: {config.BASE_URL}/sitemap.xml"
