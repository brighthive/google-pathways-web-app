import json
import os


class TestingConfiguration(object):
    """Configuration class for local development."""

    def __init__(self):
        self.debug = True
        self.testing = True

        self.CONTAINER_NAME = "test_postgres_service"
        self.IMAGE_NAME = "postgres"
        self.IMAGE_VERSION = "12"

        self.BASE_URL = "http://0.0.0.0:8000"
        self.PSQL_USER = "dt_admin_test"
        self.PSQL_PASSWORD = "passw0rd"
        self.PSQL_HOSTNAME = "localhost"
        self.PSQL_PORT = "10031"
        self.PSQL_DATABASE = "pathways_test"

        self.SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            self.PSQL_USER,
            self.PSQL_PASSWORD,
            self.PSQL_HOSTNAME,
            self.PSQL_PORT,
            self.PSQL_DATABASE,
        )
                
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        
class JenkinsConfiguration(object):
    """Configuration class for local development."""

    def __init__(self):
        self.debug = True
        self.testing = True

        self.CONTAINER_NAME = "test_postgres_service"
        self.IMAGE_NAME = "postgres"
        self.IMAGE_VERSION = "12"

        self.BASE_URL = "http://0.0.0.0:8000"
        self.PSQL_USER = "dt_admin_test"
        self.PSQL_PASSWORD = "passw0rd"
        self.PSQL_HOSTNAME = os.getenv('DB_PORT_5432_TCP_ADDR', '0.0.0.0')
        self.PSQL_PORT = os.getenv('DB_PORT_5432_TCP_PORT', 5432)
        self.PSQL_DATABASE = "pathways_test"

        self.SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            self.PSQL_USER,
            self.PSQL_PASSWORD,
            self.PSQL_HOSTNAME,
            self.PSQL_PORT,
            self.PSQL_DATABASE,
        )
                
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfiguration(object):
    """Configuration class for local development."""

    def __init__(self):
        self.debug = True
        self.testing = True

        self.BASE_URL = "http://0.0.0.0:8000"
        self.PSQL_USER = "brighthive_admin"
        self.PSQL_PASSWORD = "passw0rd"
        # self.BASE_URL = os.getenv("BASE_URL", "")
        # self.PSQL_USER = os.getenv("PSQL_USER", "")
        # self.PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "")
        self.PSQL_HOSTNAME = "postgres_service"
        self.PSQL_PORT = "5432"
        self.PSQL_DATABASE = "pathways"

        self.SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            self.PSQL_USER,
            self.PSQL_PASSWORD,
            self.PSQL_HOSTNAME,
            self.PSQL_PORT,
            self.PSQL_DATABASE,
        )
                
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfiguration(object):
    """Configuratuon class for production deployment."""

    def __init__(self):
        self.debug = False
        self.testing = False

        self.BASE_URL = os.getenv("BASE_URL", "")
        self.PSQL_USER = os.getenv("PSQL_USER", "")
        self.PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "")
        self.PSQL_HOSTNAME = os.getenv("PSQL_HOSTNAME", "")
        self.PSQL_PORT = os.getenv("PSQL_PORT", "")
        self.PSQL_DATABASE = os.getenv("PSQL_DATABASE", "")

        self.SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            self.PSQL_USER,
            self.PSQL_PASSWORD,
            self.PSQL_HOSTNAME,
            self.PSQL_PORT,
            self.PSQL_DATABASE,
        )
                
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigurationFactory(object):
    @staticmethod
    def get_config(config_type: str):
        if config_type.upper() == "TESTING":
            is_jenkins = bool(int(os.getenv('IS_JENKINS_TEST', '0')))
            if is_jenkins:
                return JenkinsConfiguration()
            else:
                return TestingConfiguration()
        if config_type.upper() == "LOCAL":
            return LocalConfiguration()
        if config_type.upper() == "PRODUCTION":
            return ProductionConfiguration()

    @staticmethod
    def from_env():
        """Retrieve configuration based on environment settings.

        Provides a configuration object based on the settings found in the `APP_ENV` variable. Defaults to the `local`
        environment if the variable is not set.
        Returns:
            object: Configuration object based on the configuration environment found in the `APP_ENV` environment variable.
        """
        environment = os.getenv("APP_ENV", "LOCAL")

        return ConfigurationFactory.get_config(environment)
