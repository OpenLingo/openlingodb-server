from app import app
from config import ROUTE_PREFIX
from flask import jsonify, request
from services import language as service


@app.route(ROUTE_PREFIX + "language", methods=['GET'])
def get_languages():
    languages = service.get_all_languages()
    if not languages:
        return "404 not found", 404
    return jsonify(languages)
