from flask_restful import Resource

from google_pathways_api.db.models import PathwaysProgram
from google_pathways_api.utils.errors import PathwaysProgramDoesNotExist
from google_pathways_api.config.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


class Pathways(Resource):
    def get(self):
        '''
        Returns all instances of the PathwaysProgram model.
        '''
        offset = 0
        limit = config.page_limit
        args = request.args

        try:
            offset = request.args['offset']
        except Exception:
            pass

        try:
            limit = request.args['limit']
        except Exception:
            pass

        return {'test': 'data'}, 200
    


class PathwaysDetail(Resource):
    def get(self, pathways_program_id: str):
        pathways_program = PathwaysProgram.query.filter_by(pathways_program_id=pathways_program_id).first()
        if not pathways_program:
            raise PathwaysProgramDoesNotExist
        
        pathways_program_json_ld = pathways_program['pathways_program']

        return pathways_program_json_ld, 200
