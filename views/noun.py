from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import noun


@app.route(ROUTE_PREFIX + "noun")
def get_all_nouns():
    return jsonify(noun.get_all_nouns())

