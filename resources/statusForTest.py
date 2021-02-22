from flask import Response,request
from flask_restful import Resource

class StatusTest(Resource):
    def get(self):
        return Response({"running: signUp,login"},status=200)
