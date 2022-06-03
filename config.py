"""Flask configuration."""
import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""

    ELASTIC_ACTIVE = os.environ.get("ELASTIC_ACTIVE")
    ELASTIC_SCHEME = os.environ.get("ELASTIC_SCHEME")
    ELASTIC_HOST = os.environ.get("ELASTIC_HOST")
    ELASTIC_PORT = os.environ.get("ELASTIC_PORT")

    LOGSTASH_ACTIVE = os.environ.get("LOGSTASH_ACTIVE")
    LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST")
    LOGSTASH_DB_PATH = os.environ.get("LOGSTASH_DB_PATH")
    LOGSTASH_TRANSPORT = os.environ.get("LOGSTASH_TRANSPORT")
    LOGSTASH_PORT = os.environ.get("LOGSTASH_PORT")

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


config = {
    'dev': DevConfig,
    'prod': ProdConfig
}
