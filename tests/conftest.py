import json
import os

import pytest
from flask_migrate import upgrade

import docker
from google_pathways_api.app import create_app
from google_pathways_api.db.models import PathwaysProgram, db
from google_pathways_api.config.config import ConfigurationFactory



class PostgreSQLContainer:
    """A PostgreSQL Container Object.
    This class provides a mechanism for managing PostgreSQL Docker containers
    so that it can be injected into unit tests.
    Class Attributes:
        config (object): A Configuration Factory object.
        container (object): The Docker container object.
        for schema_dict in schema_dicts:
            docker_client (object): Docker client.
            db_environment (list): Database environment configuration variables.
            db_ports (dict): Dictionary of database port mappings.
    """

    def __init__(self):
        self.config = ConfigurationFactory.get_config("TEST")
        self.container = None
        self.docker_client = docker.from_env()
        self.db_environment = [
            "POSTGRES_USER={}".format(self.config.PSQL_USER),
            "POSTGRES_PASSWORD={}".format(self.config.PSQL_PASSWORD),
            "POSTGRES_DB={}".format(self.config.PSQL_DATABASE),
        ]
        self.db_ports = {"5432/tcp": self.config.PSQL_PORT}

    def get_postgresql_image(self):
        """Output the PostgreSQL image from the configuation.
        Returns:
            str: The PostgreSQL image name and version tag.
        """
        return "{}:{}".format(self.config.IMAGE_NAME, self.config.IMAGE_VERSION)

    def start_container(self):
        """Start PostgreSQL Container."""
        if self.get_db_if_running():
            return

        try:
            self.docker_client.images.pull(self.get_postgresql_image())
        except Exception:
            print("fail")
            # logger.exception("Failed to pull postgres image")

        self.container = self.docker_client.containers.run(
            self.get_postgresql_image(),
            detach=True,
            auto_remove=True,
            name=self.config.CONTAINER_NAME,
            environment=self.db_environment,
            ports=self.db_ports,
        )

    def stop_if_running(self):
        try:
            running = self.docker_client.containers.get(self.config.CONTAINER_NAME)
            # logger.info(f"Killing running container '{self.config.CONTAINER_NAME}'")
            running.stop()
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return
            raise e

    def get_db_if_running(self):
        """Returns None or the db."""
        try:
            return self.docker_client.containers.get(self.config.CONTAINER_NAME)
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return



@pytest.fixture(scope="session", autouse=True)
def run_the_database(autouse=True):
    postgres = PostgreSQLContainer()
    yield postgres.start_container()
    postgres.stop_if_running()



@pytest.fixture
def app():
    os.environ['APP_ENV'] = 'TEST'
    app = create_app()

    return app 


@pytest.fixture
def pathways_programs(app):
    '''
    A fixture that adds two programs to the database.
    '''
    json_ld = {
        "@context": "http://schema.org/",
        "@type": "EducationalOccupationalProgram",
        "name": "Certified Nursing Assistant Program",
        "description": "This course helps participants cultivate the attitudes, skills and behaviors of a competent caregiver"
    }

    program_data = { 'id': '5f109a01-87c6', 'updated_at': '2020-03-23 15:10:50', 'pathways_program': json.dumps(json_ld) }
    program_one = PathwaysProgram(**program_data)

    json_ld = {
        "@context": "http://schema.org/",
        "@type": "WorkBasedProgram",
        "name": "Customer Service and Sales Training",
        "description": "Provides training in Customer Service and Sales"
    }

    program_data = { 'id': '663dfe-4aca', 'updated_at': '2020-02-01 1:31:10', 'pathways_program': json.dumps(json_ld) }
    program_two = PathwaysProgram(**program_data)

    with app.app_context():
        db.session.add(program_one)
        db.session.add(program_two)
        db.session.commit()
