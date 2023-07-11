from flask import Flask
from flask_cors import CORS

app = Flask("openlingodb")
app.config.from_pyfile('config.py')
CORS(app)
