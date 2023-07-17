from app import app
from config import ROUTE_PREFIX
from flask import jsonify, request
from services import noun as service


@app.route(ROUTE_PREFIX + "noun", methods=['GET'])
def get_nouns():
    nouns = service.get_all_nouns()
    if not nouns:
        return "404 not found", 404
    return jsonify(nouns)


@app.route(ROUTE_PREFIX + "noun/<int:noun_id>", methods=['GET'])
def get_noun_by_id(noun_id):

    noun = service.get_noun_by_id(noun_id)

    if not noun:
        return "404 not found", 404
    return jsonify(noun)


@app.route(ROUTE_PREFIX + "noun/insert", methods=['PUT'])
def insert_noun():
    data = request.get_json()
    service.insert_noun(data)
    return "s", 200


@app.route(ROUTE_PREFIX + "noun/update<int:noun_id>", methods=['PUT'])
def update_noun(noun_id: int):
    data = request.get_json()
    service.update_noun(data)
    return "s", 200
