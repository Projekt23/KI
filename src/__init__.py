from flask import Flask
from flasgger import Swagger

from config import config


def create_app(config_name):
    """For using dynamic environment"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    swagger = Swagger(app)

    # Import a module / component using its blueprint handler variable
    from src.synonymgen.controllers import mod as synonymgen_module
    from src.descriptgen.controllers import mod as descriptgen_module

    # Register blueprint(s)
    app.register_blueprint(synonymgen_module)
    app.register_blueprint(descriptgen_module)

    return app
