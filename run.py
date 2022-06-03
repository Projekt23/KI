"""Run server"""
import os
import unittest
import nltk
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from dotenv import load_dotenv
from src import create_app

load_dotenv()  # take environment variables from .env.

# if os.environ.get('KI_BACKEND') == 'prod':
#    app = DispatcherMiddleware(create_app(os.environ.get("KI_BACKEND")), {
#        '/': create_app('prod')
#    })
# else:
#    app = create_app(os.environ.get("KI_BACKEND") or 'dev')
app = create_app(os.environ.get("KI_BACKEND"))

if __name__ == '__main__':

    nltk.download('wordnet')

    if os.environ.get('KI_BACKEND') == 'prod':
        run_simple('0.0.0.0', 5000, app,
                   use_reloader=False, use_debugger=False,
                   )
