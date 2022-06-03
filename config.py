"""Flask configuration."""
import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""

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
