import json
from datetime import datetime, timedelta

from flask import Blueprint, make_response, render_template, request, url_for

from google_pathways_api.db.models import PathwaysProgram
from google_pathways_api.utils.errors import PathwaysProgramDoesNotExist

pathways_blueprint = Blueprint("pathways", __name__)


def _has_been_modified_since(request, program_last_updated):
    has_been_modified_since = True
    try:
        # Try to get `If-Modified-Since`, and convert it to a datetime object.
        if_modified_since = request.headers["If-Modified-Since"]
        if_modified_since_as_datetime = datetime.strptime(
            if_modified_since, "%a, %d %b %Y %I:%M:%S %Z"
        )
    except Exception as err:
        pass
    else:
        # Adjust `last_updated` timestamp to account for local timestamp from master Google sheet.
        # Return a 403 if `If-Modified-Since` is greater than the adjusted `program_last_updated`.
        program_last_updated_adjusted = program_last_updated + timedelta(hours=24)
        if if_modified_since_as_datetime >= program_last_updated_adjusted:
            has_been_modified_since = False

    return has_been_modified_since


def _make_links(pathways_programs):
    next_url = ""
    if pathways_programs.has_next:
        next_url = url_for("pathways.pathways", page=pathways_programs.next_num)

    prev_url = ""
    if pathways_programs.has_prev:
        prev_url = url_for("pathways.pathways", page=pathways_programs.prev_num)

    return next_url, prev_url


@pathways_blueprint.route("/pathways", methods=["GET"])
def pathways():
    """Returns a paginated view of all Pathways-formatted programs – one
    program per page."""
    entries_per_page = 1
    page = request.args.get("page", 1, type=int)
    pathways_programs = PathwaysProgram.query.order_by(
        PathwaysProgram.updated_at.desc()
    ).paginate(page, entries_per_page, False)

    program_last_updated = pathways_programs.items[0].updated_at
    headers = {"Content-Type": "text/html", "Last-Modified": program_last_updated}

    if not _has_been_modified_since(request, program_last_updated):
        return make_response("", 304)

    next_url, prev_url = _make_links(pathways_programs)

    try:
        pathways_program_json_ld = pathways_programs.items[0].pathways_program
    except IndexError:
        pathways_program_json_ld = {}

    pathways_program_for_script_tag = json.dumps(pathways_program_json_ld)

    return make_response(
        render_template(
            "pathways.html",
            next_url=next_url,
            prev_url=prev_url,
            pathways_program_for_script_tag=pathways_program_for_script_tag,
            pathways_program_to_render=json.dumps(
                pathways_program_json_ld, sort_keys=False, indent=4
            ),
        ),
        200,
        headers,
    )
