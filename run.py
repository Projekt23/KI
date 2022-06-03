"""Run server"""
import os
import unittest

from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src import create_app

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

#if os.environ.get('KI_BACKEND') == 'prod':
#    app = DispatcherMiddleware(create_app(os.environ.get("KI_BACKEND")), {
#        '/': create_app('prod')
#    })
#else:
#    app = create_app(os.environ.get("KI_BACKEND") or 'dev')
app = create_app(os.environ.get("KI_BACKEND"))

if __name__ == '__main__':
    import nltk
    nltk.download('wordnet')

    if os.environ.get('KI_BACKEND') == 'prod':
        run_simple('0.0.0.0', 5000, app,
                   use_reloader=False, use_debugger=False,
                   )
