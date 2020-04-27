from flask import Flask
from flask_migrate import Migrate

from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import db
from google_pathways_api.resources.pathways import pathways_blueprint
from google_pathways_api.resources.static_resources import static_blueprint


def create_app():
    config = ConfigurationFactory.from_env()
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(pathways_blueprint)
    app.register_blueprint(static_blueprint)

    return app
