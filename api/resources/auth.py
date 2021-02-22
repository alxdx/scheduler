from flask import Response,request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from mongoengine.errors import NotUniqueError,DoesNotExist

from database.models import Alumno

import datetime

class SignupApi(Resource):
    def post(self):
        body=request.get_json()
        user=Alumno(**body)
        user.hash_password()
        try:
            user.save()
        except NotUniqueError as e:
            #print(type(e))
            return {"error":"la matricula o el correo ya existen"},422
        else:
            id=user.id
            return {"id": str(id)},200

class LoginApi(Resource):
    def post(self):
        body=request.get_json()
        try:
            if body.get("mail")=="":
                user=Alumno.objects.get(matricula=body.get("matricula"))
            else:
                user=Alumno.objects.get(mail=body.get("mail")) 
        except DoesNotExist:
            return {"error":"datos de usuario no encontrados"},422
        else:
            authorized=user.check_password(body.get("password"))
            if not authorized:
                return {"error":"usuario o password invalidos"},401
            expires=datetime.timedelta(days=2)
            access_token=create_access_token(identity=str(user.id),expires_delta=expires)
            return {"token":access_token},200
