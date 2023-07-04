from config import ROUTE_PREFIX
from flask import Blueprint, jsonify
from services import noun as service

bp = Blueprint('noun', __name__, url_prefix=ROUTE_PREFIX)


@bp.route("noun", methods=['GET'])
def get_all_nouns():
    nouns = service.get_all_nouns()
    if not nouns:
        return "404 not found", 404
    return jsonify(nouns)
