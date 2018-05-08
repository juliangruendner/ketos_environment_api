from flask_restful import Resource
from flask import Response

class Swagger(Resource):
    def __init__(self):
        super(Swagger, self).__init__()

    def get(self):
        resp = Response("""
            <head>
            <meta http-equiv="refresh" content="0; url=http://localhost:4999/?url=http://localhost:5001/api/swagger.json" />
            </head>""", mimetype='text/html')
        return resp
