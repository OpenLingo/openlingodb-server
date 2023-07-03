from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging

from app import app
from config import PORT
# noinspection PyUnresolvedReferences
from views import *

container = WSGIContainer(app)
http_server = HTTPServer(container, max_body_size=250000000)
http_server.listen(PORT)
enable_pretty_logging()

IOLoop.current().start()
