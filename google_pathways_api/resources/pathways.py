import json

from flask import Blueprint, make_response, render_template, request, url_for

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import PathwaysProgram
from google_pathways_api.utils.errors import PathwaysProgramDoesNotExist

config = ConfigurationFactory.from_env()

blueprint = Blueprint('pathways', __name__)


def _make_links(pathways_programs):
    next_url = ''
    if pathways_programs.has_next:
        next_url = url_for('pathways.pathways', page=pathways_programs.next_num)
    
    prev_url = ''
    if pathways_programs.has_prev:
        prev_url = url_for('pathways.pathways', page=pathways_programs.prev_num)

    return next_url, prev_url


@blueprint.route('/pathways', methods=['GET'])
def pathways():
    '''
    Returns a paginated view of all Pathways-formatted programs – one program per page.
    '''
    headers = {'Content-Type': 'text/html'}
    entries_per_page = 1
    page = request.args.get('page', 1, type=int)
    pathways_programs = PathwaysProgram.query \
        .order_by(PathwaysProgram.updated_at.desc()) \
        .paginate(page, entries_per_page, False)

    next_url, prev_url = _make_links(pathways_programs)

    try: 
        pathways_program_json_ld = pathways_programs.items[0].pathways_program
    except IndexError:
        pathways_program_json_ld = {}

    pathways_program_for_script_tag = json.dumps(pathways_program_json_ld)

    return make_response(render_template('pathways.html', 
                            next_url=next_url,
                            prev_url=prev_url,
                            pathways_program_for_script_tag=pathways_program_for_script_tag, 
                            pathways_program_to_render=json.dumps(pathways_program_json_ld, sort_keys = False, indent = 4)), 200, headers)


@blueprint.route('/sitemap.xml', methods=['GET'])
def site_map():
    pathways_programs = PathwaysProgram.query \
        .order_by(PathwaysProgram.updated_at.desc())
    
    return render_template('sitemap.xml', pathways_programs=pathways_programs, base_url=config.BASE_URL)
