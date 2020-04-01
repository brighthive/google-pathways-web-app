from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import db
from google_pathways_api.resources.pathways import Pathways



def create_app():
    config = ConfigurationFactory.from_env()
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Add resources
    api = Api(app)
    api.add_resource(Pathways, '/pathways')

    return app
