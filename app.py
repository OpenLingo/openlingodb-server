from flask import Flask
from flask_cors import CORS

app = Flask("openlingodb") # noqa (reckons there's a spelling error)
app.config.from_pyfile('config.py')
CORS(app)
