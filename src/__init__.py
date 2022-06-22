from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from config import config

from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import FlaskLogstashFormatter


def create_app(config_name):
    """For using dynamic environment"""

    # create flask app instance
    app = Flask(__name__)
    # load configuration
    app.config.from_object(config[config_name])

    app.logger.info(r"""\
    
     __  __     __        ______     ______     ______     __  __     ______     __   __     _____    
    /\ \/ /    /\ \      /\  == \   /\  __ \   /\  ___\   /\ \/ /    /\  ___\   /\ "-.\ \   /\  __-.  
    \ \  _"-.  \ \ \     \ \  __<   \ \  __ \  \ \ \____  \ \  _"-.  \ \  __\   \ \ \-.  \  \ \ \/\ \ 
     \ \_\ \_\  \ \_\     \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\\"\_\  \ \____- 
      \/_/\/_/   \/_/      \/_____/   \/_/\/_/   \/_____/   \/_/\/_/   \/_____/   \/_/ \/_/   \/____/ 
                                                                                                      
    """)
    app.logger.info("Initializing environment for " + app.config['FLASK_ENV'])
    app.logger.info("DEBUG = " + str(app.config['DEBUG']))
    app.logger.info("TESTING = " + str(app.config['TESTING']))

    # CORS allow all
    CORS(app)

    # Swagger API doc
    Swagger(app)

    # Logging
    if app.config['LOGSTASH_ACTIVE']:
        app.logger.info("Configuring LOGSTASH handler")
        logstash_handler = AsynchronousLogstashHandler(
            app.config['LOGSTASH_HOST'],
            app.config['LOGSTASH_PORT'],
            database_path=app.config['LOGSTASH_DB_PATH'],
            transport=app.config['LOGSTASH_TRANSPORT']
        )
        logstash_handler.formatter = FlaskLogstashFormatter(metadata={"beat": "flask-ki_backend"})
        app.logger.addHandler(logstash_handler)
        app.logger.info("--- LOGSTASH CONNECT ---")

    app.logger.info("Register Blueprints")

    # Import a module / component using its blueprint handler variable
    from src.synonymgen.controllers import mod as synonymgen_module
    from src.descriptgen.controllers import mod as descriptgen_module

    # Register blueprint(s)
    app.register_blueprint(synonymgen_module)
    app.register_blueprint(descriptgen_module)

    app.logger.info("--- FINISHED STARTUP ---")
    return app
