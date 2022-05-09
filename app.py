from flask import Flask
from synonym_check_svc import SynonymsFromWordnet

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/test-synonym/<term>')
def hello_world(term):
    return SynonymsFromWordnet(term)


if __name__ == '__main__':
    app.run()
