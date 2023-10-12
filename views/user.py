from app import app, ROUTE_PREFIX
from flask import jsonify, request
from services import user as service


@app.route(ROUTE_PREFIX + "user")
def get_all_user():
    return jsonify(service.get_all_users())


@app.route(ROUTE_PREFIX + "user/<string:email>")
def get_user_by_email(email: str):
    u = service.find_user(email)

    if not u:
        return "404 Not Found", 404
    return jsonify(u)


@app.route(ROUTE_PREFIX + "user/insert", methods=['PUT'])
def insert_user():

    data = request.get_json()
    print(data)

    service.insert_user(data)
    return "success", 200
