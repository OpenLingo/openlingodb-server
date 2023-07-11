from app import app
from config import HOST
from views import *  # noqa


@app.route("/")
def hello():
    return "<p>Server is up.</p>"


if __name__ == "__main__":
    print("Starting OpenLingo from ", __file__)
    app.run(debug=True, host=HOST)
    