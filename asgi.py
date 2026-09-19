from a2wsgi import WSGIMiddleware
from app import app

# Wrap the Flask WSGI app into an ASGI application
asgi_app = WSGIMiddleware(app)