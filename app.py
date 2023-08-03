from devfu.db import Database
from devfu.flask import DevFUFlask
from flask_cors import CORS

ROUTE_PREFIX = '/api/'


class OpenLingoDBApp(DevFUFlask):
    def __init__(self, *args, **kwargs):
        DevFUFlask.__init__(self, *args, **kwargs)
        self.json_encoder.decimal_converter = float
        self.json_encoder.date_as_datetime = False
        self.framework_version = (0, 0, 62)
        print("App created")


app = OpenLingoDBApp(__name__)
app.config.from_pyfile('config.py')
CORS(app)

Database.init(app, retry_count=1)
