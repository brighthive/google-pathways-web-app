from flask import Blueprint, render_template

from google_pathways_web_app.config.config import ConfigurationFactory
from google_pathways_web_app.db.models import PathwaysProgram

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
    """Returns `robots.txt` data, which tells the Google crawlers where to find
    the Sitemap.

    We use a route that returns dynamically constructed text (rather
    than serving a static file) because the Sitemap property MUST BE an
    absolute path. This solution accounts for the multiple deployment
    environments and domain namespaces BrightHive manages.
    """

    robots_dot_txt = f"User-agent: google \nUser-agent: googlebot \nAllow: / \n\nUser-agent: * \nDisallow: / \n\nSitemap: {config.BASE_URL}/sitemap.xml"
    return robots_dot_txt
