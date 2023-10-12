from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import level as service


@app.route(ROUTE_PREFIX + "level", methods=['GET'])
def get_levels():
    """
    Return(s):
    jsonify(data) -> A json string.

    Route:
    http://127.0.0.1:5000/api/level
    """
    data = service.get_all_levels()

    if not data:
        return "404 not found", 404
    return jsonify(data)
