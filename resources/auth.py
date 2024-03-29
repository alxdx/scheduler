from flask import Response,request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from mongoengine.errors import NotUniqueError,DoesNotExist

from database.models import Alumno

import datetime, random


class SignupApi(Resource):
    def post(self):
        body=request.get_json()
        if body.get("password") != body.get("confirmPassword"):
            return {"error":"las contraseñas son diferentes"},422
        
        user=Alumno(
                   matricula = body.get('matricula'), 
                   name = body.get('name'),
                   mail = body.get('mail'),
                   carrera= body.get('carrera'),
                   password  = body.get('password') 
                )
        # TODO hay que validar cada dato del body
        user.carrera = user.carrera.upper()
        user.hash_password()
        if "materias_cursadas" in body and len(body.get("materias_cursadas")) > 0:
            user.last_updated = datetime.date.today()
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
            if "mail" not in body or body.get("mail")=="":
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
            if user.last_updated != None:
                l_u =  user.last_updated.strftime('%d-%m-%Y')
            else:
                l_u = None
            payload= {
                    "token":access_token,
                    "matricula": user.matricula,
                    "name":user.name,
                    "carrera":user.carrera,
                    "last_updated": l_u
                    }
            return payload,200

