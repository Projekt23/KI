"""Controllers for synonym generation"""
from flask import Blueprint, json
from flask import current_app, request

from .services import get_synonyms_wordnet, get_synonyms_wordhoard

mod = Blueprint('synonymgen', __name__, url_prefix='/synonymgen')


@mod.route('/generatesynonyms', methods=['POST'])
def generate_synonyms():
    """
    Generates a list of synonyms for a term.
    ---
    parameters:
    definitions:
        SynonymList:
            type: array
            items: string
    responses:
        200:
            description: A list of synonyms
            schema:
                $ref: '#/definitions/SynonymList'
            examples:
                invoice: ['bill','receipt']
    """

    data = request.get_json()
    if not isinstance(data.get('term'), str):
        result = {
            'error': True,
            'error_msg': 'Request body must contain key "term" with string value.'
        }
    else:
        result_list = []
        if data.get('method') == 'wordnet':
            result_list = get_synonyms_wordnet(data['term'])
        else:
            data['method'] = 'wordhoard'
            result_list = get_synonyms_wordhoard(data['term'])

        result = {
            'synonyms': result_list,
            'method': data['method']
        }

    response = current_app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

    return response
