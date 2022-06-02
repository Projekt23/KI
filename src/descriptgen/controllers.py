from flask import Blueprint, render_template, json
from flask import current_app, request

mod = Blueprint('descriptgen', __name__, url_prefix='/descriptgen')


@mod.route('/generatedescription', methods=['POST'])
def generate_description():
    data = request.get_json()

    return ''


@mod.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()

    result = {}
    response = current_app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response
