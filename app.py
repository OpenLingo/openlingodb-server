from flask import Flask
from views import *

app = Flask("__name__")
app.config.from_pyfile('config.py')

app.register_blueprint(noun.bp)
app.register_blueprint(user.bp)
