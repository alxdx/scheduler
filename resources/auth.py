from flask import Response,request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from mongoengine.errors import NotUniqueError,DoesNotExist

from database.models import Alumno

import datetime, random


class SignupApi(Resource):
    def post(self):
        body=request.get_json()
        user=Alumno(**body)
        user.hash_password()
        user["carrera"]="null"
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
            ul_act=self.random_date();
            payload= {
                    "token":access_token,
                    "matricula": user.matricula,
                    "name":user.name,
                    "carrera":user.carrera,
                    "ultima_actualizacion":ul_act
                    }
            return payload,200

    
    #temp func
    def random_date(self):
        #year/month/date
        start_date = datetime.date(2021, 3, 1)
        end_date = datetime.date(2021, 5, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date.strftime('%d-%m-%Y')