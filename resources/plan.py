from flask import Response,make_response
from flask_restful import Resource, request
from database.models import Plan,Materia
import re
from bson import regex
#clase que retorna todo el programa academico de una carrera
#parametros que puede recibir son ITI || LCC || ICC
class Plan_r(Resource):

    def valid_param(self,carrera=None,nivel=None) -> bool:
        values_carrera = ["LCC","ICC","ITI"]
        values_nivel =   ["formativo","basico","optativas"]
        if carrera is not None and carrera in values_carrera:
            return True
        if nivel is not None and nivel in values_nivel:
            return True
        return False

    def get_all(self,carrera):
        reg=regex.Regex.from_native(re.compile(carrera,re.IGNORECASE))
        pipeline=[
                {"$match":{"carrera":{"$regex":reg }}},
                {"$sort":{"carrera":-1}},
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
                            "in":{"$concatArrays":["$$this","$$value"]}
                            }
                        }
                    }
                }]
        ans=list(Plan.objects().aggregate(pipeline))
        return ans

    def get_basico(self,carrera):
        pipeline=[
            {"$match":{"carrera":carrera +"-SEM-BASICO"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return ans

    def get_formativo(self,carrera):
        pipeline=[
            {"$match":{"carrera":carrera +"-SEM-FORMATIVO"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return ans

    def get_optativas(self,carrera):
        pipeline=[
                {"$match":{"carrera" :carrera +"-SEM-OPTATIVAS"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return ans

    def get(self):
        carrera=request.args.get("carrera").upper()
        nivel= request.args.get("nivel")
        ans=None
        if self.valid_param(carrera=carrera) and nivel is None:
            ans = self.get_all(carrera)
        elif self.valid_param(carrera=carrera) and self.valid_param(nivel=nivel):
            nivel=nivel.upper()
            print(nivel)
            if nivel == "BASICO":
                ans = self.get_basico(carrera)
            elif nivel == "FORMATIVO":
                ans = self.get_formativo(carrera)
            elif nivel == "OPTATIVAS":
                ans = self.get_optativas(carrera)
        if ans is not None:
            return make_response(ans[0],200)
        else:
            return make_response({"error": "parametros de query no reconocidos"},400)

