from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import dialect as service


@app.route(ROUTE_PREFIX + "dialect", methods=['GET'])
def get_dialects():
    """
    Return(s):
    jsonify(definitions) -> A json string.

    Route:
    http://127.0.0.1:5000/api/definition/noun_id
    """
    data = service.get_all_dialects()

    if not data:
        return "404 not found", 404
    return jsonify(data)


@app.route(ROUTE_PREFIX + "dialect/<int:dialect_id>", methods=['GET'])
def get_dialect(dialect_id):

    data = service.get_dialect(dialect_id)

    if not data:
        return "404 not found", 404
    return jsonify(data)


@app.route(ROUTE_PREFIX + "dialect/get_by_language/<int:language_id>", methods=['GET'])
def get_language_dialects(language_id):

    data = service.get_dialects_by_language(language_id)

    if not data:
        return "404 not found", 404
    return jsonify(data)
