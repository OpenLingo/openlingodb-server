from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import user_language as service


@app.route(ROUTE_PREFIX + "user_language/insert", methods=['PUT'])
def insert_user_language():

    data = request.get_json()

    service.insert_user_language(data)
    return "success", 200
