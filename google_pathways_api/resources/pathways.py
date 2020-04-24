import json

from flask import make_response, render_template, request, url_for
from flask_restful import Resource

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import PathwaysProgram
from google_pathways_api.utils.errors import PathwaysProgramDoesNotExist

config = ConfigurationFactory.from_env()


class Pathways(Resource):
    def _make_links(self, pathways_programs):
        next_url = ''
        if pathways_programs.has_next:
            next_url = url_for('pathways', page=pathways_programs.next_num)
        
        prev_url = ''
        if pathways_programs.has_prev:
            prev_url = url_for('pathways', page=pathways_programs.prev_num)

        return next_url, prev_url

    def get(self):
        '''
        Returns a paginated view of all Pathways-formatted programs – one program per page.
        '''
        headers = {'Content-Type': 'text/html'}
        entries_per_page = 1
        page = request.args.get('page', 1, type=int)
        pathways_programs = PathwaysProgram.query \
            .order_by(PathwaysProgram.updated_at.desc()) \
            .paginate(page, entries_per_page, False)

        next_url, prev_url = self._make_links(pathways_programs)

        try: 
            pathways_program_json_ld = pathways_programs.items[0].pathways_program
        except IndexError:
            pathways_program_json_ld = {}

        pathways_program_for_script_tag = json.dumps(pathways_program_json_ld)

        return make_response(render_template('pathways.html', 
                                next_url=next_url,
                                prev_url=prev_url,
                                pathways_programs_for_script_tag=pathways_program_for_script_tag, 
                                pathways_program_to_render=json.dumps(pathways_program_json_ld, sort_keys = False, indent = 4)), 200, headers)


