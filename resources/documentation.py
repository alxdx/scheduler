from flask_restful import Resource
from flask import send_from_directory

class Documentacion(Resource):
    def get(self):
        return send_from_directory("docs","api-spec-v1.html")
