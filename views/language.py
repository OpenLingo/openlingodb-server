from app import app, ROUTE_PREFIX
from flask import jsonify
from services import language as service


@app.route(ROUTE_PREFIX + "language", methods=['GET'])
def get_languages():
    """
    Return(s):
    jsonify(language) -> A json string.

    Route:
    http://127.0.0.1:5000/api/language
    """
    languages = service.get_all_languages()

    if not languages:
        return "404 not found", 404
    return jsonify(languages)


@app.route(ROUTE_PREFIX + "language/<int:language_id>", methods=['GET'])
def get_language(language_id: int):
    """
    Parameter(s):
    language_id (mandatory) -> The id of the language being fetched. Comes from the route

    Return(s):
             jsonify(language) -> A json string.

    Route:
    http://127.0.0.1:5000/api/language/id
    where 'id' is the id of the requested language.
    """
    language = service.get_language(language_id)

    if not language:
        return "langauge not found", 404
    return jsonify(language)
