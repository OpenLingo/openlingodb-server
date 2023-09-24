from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import noun as service


@app.route(ROUTE_PREFIX + "noun", methods=['GET'])
def get_nouns():
    """
    Return(s):
    jsonify(nouns) -> A json string.

    Route:
    http://127.0.0.1:5000/api/noun
    """
    nouns = service.get_all_nouns()

    if not nouns:
        return "404 not found", 404
    return jsonify(nouns)


@app.route(ROUTE_PREFIX + "noun/<int:noun_id>", methods=['GET'])
def get_noun_by_id(noun_id):
    """
    Parameter(s):
    noun_id (mandatory) -> The id of the noun being fetched. Comes from the route

    Return(s):
         jsonify(nouns) -> A json string.

    Route:
    http://127.0.0.1:5000/api/noun/id
    where 'id' is the id of the requested noun.
    """
    noun = service.get_noun_by_id(noun_id)

    if not noun:
        return "404 not found", 404
    return jsonify(noun)


@app.route(ROUTE_PREFIX + 'noun/search/<string:search_term>', methods=['GET'])
def get_noun_by_string(search_term):

    return service.get_nouns_by_string(search_term)


@app.route(ROUTE_PREFIX + "noun/insert", methods=['PUT'])
def insert_noun():
    """
    Parameter(s): Requires that any data to be inserted be sent via http using the
                  PUT method.

    Return(s): A http response for the client to make use of.

    Route:
    http://127.0.0.1:5000/api/insert
    """
    data = request.get_json()
    print(data)
    service.insert_noun(data)
    return "success", 200


@app.route(ROUTE_PREFIX + "noun/update<int:noun_id>", methods=['PUT'])
def update_noun(noun_id: int):
    """
    Parameter(s): Requires that any data to be inserted be sent via http using the
                  PUT method.

    Return(s): A http response for the client to make use of.

    Route:
    http://127.0.0.1:5000/api/update
    """
    data = request.get_json()

    service.update_noun(data)
    return "success", 200
