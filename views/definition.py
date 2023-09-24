from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import definition as service


@app.route(ROUTE_PREFIX + "definition/<int:noun_id>", methods=['GET'])
def get_definitions(noun_id):
    """
    Return(s):
    jsonify(definitions) -> A json string.

    Route:
    http://127.0.0.1:5000/api/definition/noun_id
    """
    data = service.get_definitions(noun_id)

    if not data:
        return "404 not found", 404
    return jsonify(data)


@app.route(ROUTE_PREFIX + "definition/insert", methods=['PUT'])
def insert_definition():

    data = request.get_json()
    service.insert_definition(data)
    return "success", 200


@app.route(ROUTE_PREFIX + "definition/delete", methods=['PUT'])
def delete_definition():

    data = request.get_json()
    service.delete_definition(data)
    return "success", 200
