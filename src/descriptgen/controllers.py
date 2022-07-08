"""Controllers for description generation"""
from flask import Blueprint, json
from flask import current_app, request

from .services import summarize_text, get_wiki_text

mod = Blueprint('descriptgen', __name__, url_prefix='/descriptgen')


@mod.route('/generatedescription', methods=['POST'])
def generate_description():
    """
    Generates a description for a provided term by searching for and summarizing a corresponding wikipedia article.
    ---
    parameters:
    definitions:
        DescriptionResp:
            type: array
            items: string
    responses:
        200:
            description: A description of
            schema:
                $ref: '#/definitions/SynonymList'
            examples:
                invoice: {"description": "This is a test description."}
    """

    data = request.get_json()

    if not isinstance(data.get('term'), str):
        result = {
            'error': True,
            'error_msg': 'Request body must contain attribute term with string value.'
        }
    elif isinstance(data.get('sent'), int) and int(data.get('sent')) < 0:
        result = {
            'error': True,
            'error_msg': 'Sentence length of summary must be greater 0.'
        }
    else:
        data['lang'] = data.get('lang') or 'en'
        data['sent'] = data.get('sent') or 5
        summary = get_wiki_text(data.get('term'), sent=data['sent'], lang=data['lang'])
        result = {
            'summary': summary[0],
            'sent': summary[1],
            'lang': data['lang'],
            'method': 'spaCy'
        }


    response = current_app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


@mod.route('/summarize', methods=['POST'])
def summarize():
    """
    Generates a summary for a provided text. Can be configured to choose between different languages and summarization techniques.
    ---
    parameters:
    definitions:
        DescriptionResp:
            type: object
            properties:
                summary:
                    type: string
                lang:
                    type: string
                sent:
                    type: integer
    responses:
        200:
            description: A summary of the provided text
            schema:
                $ref: '#/definitions/DescriptionResp'
            examples:
                invoice: {"description": "This is a test description."}
    """

    data = request.get_json()
    if not isinstance(data.get('text'), str):
        result = {
            'error': True,
            'error_msg': 'Request body must contain attribute text with string value.'
        }
    elif isinstance(data.get('sent'), int) and int(data.get('sent')) < 0:
        result = {
            'error': True,
            'error_msg': 'Sentence length of summary must be greater 0.'
        }
    else:
        data['lang'] = data.get('lang') or 'en'
        data['sent'] = data.get('sent') or 5
        summary = summarize_text(data['text'], sent=data['sent'], lang=data['lang'])

        result = {'summary': summary[0], 'lang': data['lang'], 'sent': summary[1]}

    response = current_app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response
