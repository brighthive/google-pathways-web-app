import json
import os


class ConfigurationError(Exception):
    pass


class Configuration(object):
    def find_json_config_file(self):
        """Find JSON configuration file.
        Locate the JSON configuration relative to the application path.
        Returns:
            str: Configuration file.
        Raises:
            ConfigurationError: If the configuration file cannot be found.
        """

        absolute_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(absolute_path, 'config.json')

        if os.path.exists(config_file) and os.path.isfile(config_file):
            return config_file
        else:
            raise ConfigurationError(
                'Cannot find configuration file in path {}.'.format(absolute_path))

    def load_json_config(self, config_file: str):
        """Load application configuration from JSON file.
        Args:
            config_file (str): The path and name of the configuration file to load.
        Returns:
            dict: Configuration object.
        Raises:
            ConfigurationError: If the configuration file doesn't exist or
                cannot be loaded because of a syntax error.
        """

        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            raise ConfigurationError(
                'Error loading configuration file {}.'.format(config_file))

        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception:
            raise ConfigurationError(
                'Failed to load configuration file {}. Please check the configuration file.'.format(config_file))

    def from_json(self, environment='local'):
        """Load application configuration from JSON object based on the configuration type.
        Args:
            environment (str): The environment to load.
        Raises:
            ConfigurationError: If the JSON configuration cannot be loaded.
        """

        config_file = self.find_json_config_file()
        data = self.load_json_config(config_file)

        if environment in data.keys():
            fields = data[environment]
            try:
                self.PSQL_USER = fields['psql_user']
                self.PSQL_PASSWORD = fields['psql_password']
                self.PSQL_HOSTNAME = fields['psql_hostname']
                self.PSQL_PORT = fields['psql_port']
                self.PSQL_DATEBASE = fields['psql_database']
                
                self.environment = environment
                self.debug = True
                self.testing = True
            except Exception:
                raise ConfigurationError(
                    'Invalid key in JSON configuration. Please check the configuration.')
            else:
                self.SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
                    self.PSQL_USER,
                    self.PSQL_PASSWORD,
                    self.PSQL_HOSTNAME,
                    self.PSQL_PORT,
                    self.PSQL_DATEBASE
                )

        else:
            raise ConfigurationError(
                'Cannot find environment \'{}\' in JSON configuration.')


class LocalConfiguration(Configuration):
    """Configuration class for local development."""
    def __init__(self):
        self.from_json('local')
        self.debug = True
        self.testing = True


class DevelopmentTestingConfiguration(Configuration):
    """Configuration class for deployment of app on the Dev Testing server."""

    def __init__(self):
        self.from_json('development_testing')
        self.debug = True
        self.testing = False


class ProductionConfiguration(Configuration):
    """Configuratuon class for production deployment."""

    def __init__(self):
        self.from_json('production')
        self.debug = False
        self.testing = False


class ConfigurationFactory(object):
    @staticmethod
    def get_config(config_type: str):
        if config_type.upper() == 'LOCAL':
            return LocalConfiguration()
        if config_type.upper() == 'DEVELOPMENT_TESTING':
            return DevelopmentTestingConfiguration()
        if config_type.upper() == 'PRODUCTION':
            return ProductionConfiguration()

    @staticmethod
    def from_env():
        """Retrieve configuration based on environment settings.
        Provides a configuration object based on the settings found in the `APP_ENV` variable. Defaults to the `local`
        environment if the variable is not set.
        Returns:
            object: Configuration object based on the configuration environment found in the `APP_ENV` environment variable.
        """
        environment = os.getenv('APP_ENV', 'LOCAL')

        return ConfigurationFactory.get_config(environment)