from config import ROUTE_PREFIX
from flask import Blueprint, jsonify
from services import user as service

bp = Blueprint('user', __name__, url_prefix=ROUTE_PREFIX)


@bp.route(ROUTE_PREFIX + "user")
def get_all_user():
    return jsonify(service.get_all_users())


@bp.route(ROUTE_PREFIX + "user/<string:email>")
def get_user_by_email(email: str):
    u = service.find_user(email)
    if not u:
        return "404 Not Found", 404

    return jsonify(u)
