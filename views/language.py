from app import app
from config import ROUTE_PREFIX
from flask import jsonify
from services import language as service


@app.route(ROUTE_PREFIX + "language", methods=['GET'])
def get_languages():
    languages = service.get_all_languages()

    if not languages:
        return "404 not found", 404
    return jsonify(languages)


@app.route(ROUTE_PREFIX + "language/<int:language_id>", methods=['GET'])
def get_language(language_id: int):
    language = service.get_language(language_id)

    if not language:
        return "langauge not found", 404
    return jsonify(language)
