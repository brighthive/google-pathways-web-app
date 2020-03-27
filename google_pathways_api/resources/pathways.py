from flask_restful import Resource

class Pathways(Resource):
    def get(self):
        return 'Hello, world!'