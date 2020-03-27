from flask import Flask
from flask_restful import Api

from google_pathways_api.resources.pathways import Pathways


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Pathways, '/pathways')

    return app