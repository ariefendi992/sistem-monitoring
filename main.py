import asyncio
import os
from app import create_app
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve

"""
    Flask with granian
    cli comman:
        granian --interface wsgi|asgi|rsgi --reload main:myApp
        granian --interface wsgi --reload --ssl-certificate certificate.crt --ssl-keyfile private.key --host ['0.0.0.0','0.0.0.0'] --port [80,443] --port 443 main:myApp
        granian --interface wsgi --reload --ssl-certificate certificate.crt --ssl-keyfile private.key --host 0.0.0.0 --port 80 --port 443 main:myApp
"""
myApp = create_app()

"""
    RUN with hypercorn http redirect to https 
    hypercorn --certfile cert/certificate.crt --keyfile cert/private.key --bind 0.0.0.0:443 --insecure-bind 0.0.0.0:80 main:app 
    
"""
app = WsgiToAsgi(myApp)

# cert = os.getcwd() + "/cert/certificate.crt"
# key = os.getcwd() + "/cert/private.key"
# config = Config()
# config.certfile("/cert/certificate.crt")
# config.keyfile("/cert/private.key")
# config.bind = ["localhost:443"]
# config.insecure_bind = ["localhost:80"]
# asyncio.run(serve(myApp, config=config))
