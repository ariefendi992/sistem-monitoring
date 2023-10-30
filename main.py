from app import create_app
from asgiref.wsgi import WsgiToAsgi

"""
    Flask with granian
    cli comman:
        granian --interface wsgi|asgi|rsgi --reload main:myApp
"""
asgiApp = WsgiToAsgi(create_app())
myApp = create_app()
