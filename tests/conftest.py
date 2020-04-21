import json
import logging
import os
from time import sleep

import docker
import pytest
from flask_migrate import upgrade

from google_pathways_api.app import create_app
from google_pathways_api.config.config import ConfigurationFactory
from google_pathways_api.db.models import PathwaysProgram, db

os.environ['APP_ENV'] = 'TEST'
testing_app = create_app()


@pytest.fixture
def app():
    """
    This test suite uses `pytest-flask`. 
    `pytest-flask` comes with an out-of-the-box test `client` fixture (i.e., an instance of flask.Flask.test_client).
    The client fixture is nifty: it pushes the request context to tests, so you can access context-bound objects
    without a context manager.

    However, the pytest-flask `client` fixture expects an `app` fixture – provided here.
    """
    return testing_app 


class PostgreSQLContainer:
    """A PostgreSQL Container Object.
    This class provides a mechanism for managing PostgreSQL Docker containers
    so that a database can be injected into tests.
    Class Attributes:
        config (object): A Configuration Factory object.
        container (object): The Docker container object.
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
            "POSTGRES_DB={}".format(self.config.PSQL_DATABASE)
        ]
        self.db_ports = {"5432/tcp": self.config.PSQL_PORT}

    def get_postgresql_image(self):
        """Output the PostgreSQL image from the configuration.
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
            logging.error("Failed to pull postgres image")
            raise RuntimeError

        self.container = self.docker_client.containers.run(
            self.get_postgresql_image(),
            detach=True,
            auto_remove=True,
            name=self.config.CONTAINER_NAME,
            environment=self.db_environment,
            ports=self.db_ports,
        )
        logging.info("PostgreSQL container running!")

        apply_migrations()

    def stop_if_running(self):
        try:
            running = self.docker_client.containers.get(self.config.CONTAINER_NAME)
            logging.info(f"Killing running container '{self.config.CONTAINER_NAME}'")
            running.stop()
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return
            raise e

    def get_db_if_running(self):
        """
        Return the container or None.
        """
        try:
            return self.docker_client.containers.get(self.config.CONTAINER_NAME)
        except Exception as e:
            if "404 Client Error: Not Found" in str(e):
                return


def apply_migrations():
    """Apply Database Migrations
    Applies the database migrations to the test database container.
    Args:
        config (object): Configuration object to pull the needed components from.
    """
    applied_migrations = False
    retries = 0
    max_retries = 3

    with testing_app.app_context():
        relative_path = os.path.dirname(os.path.relpath(__file__))
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        root_path = absolute_path.split(relative_path)[0]
        migrations_dir = os.path.join(
            root_path, 'migrations')

        while retries < max_retries and applied_migrations is False:
            logging.info('Attempting to apply migrations ({} of {})...'.format(
                retries + 1, max_retries))
            try:
                upgrade(directory=migrations_dir)
                applied_migrations = True
            except Exception:
                retries += 1
                sleep(2)


@pytest.fixture(scope="session", autouse=True)
def database():
    postgres = PostgreSQLContainer()
    postgres.start_container()
    yield db
    postgres.stop_if_running()


@pytest.fixture(autouse=True)
def database_session():    
    session = db.session

    yield session

    session.query(PathwaysProgram).delete()
    session.commit()
    session.remove()



@pytest.fixture
def pathways_programs(client, database_session):
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

    database_session.add(program_one)
    database_session.add(program_two)
    database_session.commit()