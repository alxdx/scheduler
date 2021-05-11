from flask import Response,make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required,get_jwt_identity

from database.models import Alumno,Plan

import re
from bson import regex
import datetime 
class PlanDeAlumno(Resource):
    def get_materias_cursadas(self,carrera,materias_aprobadas):
        reg = regex.Regex.from_native(re.compile(carrera,re.IGNORECASE))
        pipeline = [
                {"$match":{"carrera":{"$regex":reg }}},
                {"$group":{
                    "_id":0,
                    "materias":{
                        "$push":"$materias"
                        }
                    }
                },
                {"$project":{
                    "_id":0,
                    "carrera":carrera.upper(),
                    "materias":{
                        "$reduce":{
                            "input":"$materias",
                            "initialValue":[],
                            "in":{
                                "$concatArrays":["$$this","$$value"]
                            }
                        }
                    }
                }}]
        ans = list(Plan.objects().aggregate(pipeline))
        return ans
    @jwt_required()
    def get(self,matricula):
        alumno_id = get_jwt_identity()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != matricula:
            return {"msg":"la matricula no corresponde con el usuario logueado"}, 401
        if alumno.carrera == "null":
            return {"msg":"aun no has registrado una carrera"},400
        materias_cursadas = self.get_materias_cursadas(alumno.carrera,alumno.materias_cursadas)
        payload = {"matricula": alumno.matricula,
                "carrera": alumno.carrera,
                "materias": materias_cursadas,
                "last_updated": alumno.last_updated.strftime('%d-%m-%Y')
                }
        return payload,200
    @jwt_required()
    #AQUI FALTA VALIDAR QUE LA CARRERA QUE SE QUIERA AGREGAR PERTENEZCA AL PLAN DE ESTUDIOS
    def patch(self,matricula):
        values_carrera = ["LCC","ICC","ITI"]
        alumno_id = get_jwt_identity()
        alumno = Alumno.objects.get(id=alumno_id)
        body = request.get_json()
        if alumno.matricula != matricula or alumno.matricula != body["matricula"]:
            return {"msg":"la matricula no corresponde con el usuario logueado"}, 401
        if body["carrera"] not in values_carrera:
            #esto hay que agregarlo a la docu
            return {"msg":"parametros de query no reconocidos:(carrera)"},400
        if alumno.carrera == "null":
            alumno.update(carrera=body["carrera"],last_updated=datetime.date.today())
            alumno.reload()

        if alumno.carrera != body["carrera"]:
            return {"msg":"la carrera no corresponde con el usuario logueado"},401
        
        alumno.update(add_to_set__materias_cursadas = body["materias_nuevas"],last_updated=datetime.date.today())
        return 200

