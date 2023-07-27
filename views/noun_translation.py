from app import app
from config import ROUTE_PREFIX
from flask import jsonify, request
from services import noun_translation as service


@app.route(ROUTE_PREFIX + "translation/<int:noun_id>", methods=['GET'])
def get_translations(noun_id):
    """
    Return(s):
    jsonify(translations) -> A json string.

    Route:
    http://127.0.0.1:5000/api/translation/noun_id
    """
    translations = service.get_translations(noun_id)

    if not translations:
        return "404 not found", 404
    return jsonify(translations)


@app.route(ROUTE_PREFIX + "translation/insert", methods=['PUT'])
def add_translation():
    """
    Parameter(s): Requires that any data to be inserted be sent via http using the
                  PUT method.

    Return(s): A http response for the client to make use of.

    Route:
    http://127.0.0.1:5000/api/translation/add
    """
    data = request.get_json()

    service.insert_noun(data)
    return "success", 200
