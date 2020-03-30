from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import db
from google_pathways_api.resources.pathways import Pathways, PathwaysDetail

config = ConfigurationFactory.from_env()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Add resources
    api = Api(app)
    api.add_resource(Pathways, '/pathways')
    api.add_resource(PathwaysDetail, '/pathways_program_id/<string:pathways_id>')

    return app
