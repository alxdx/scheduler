from flask import Response,request,make_response
from flask_restful import Resource
from database.models import Plan,Materia
import re
from bson import regex
#clase que retorna todo el programa academico de una carrera
#parametros que puede recibir son ITI || LCC || ICC
class ProgramaCompleto(Resource):
    def get(self,carrera):
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
        #return make_response(json.dumps(ans),200)
        return make_response(ans[0],200)

#clase que retorna todo el programa formativo de una carrera
#clase que retorna todo el programa formativo de una carrera
class ProgramaFormativo(Resource):
    def get(self,carrera):
        pipeline=[
            {"$match":{"carrera":carrera.upper()+"-SEM-FORMATIVO"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return make_response(ans[0],200)
#clase que retorna todo el programa basico de una carrera
class ProgramaBasico(Resource):
    def get(self,carrera):
        pipeline=[
            {"$match":{"carrera":carrera.upper()+"-SEM-BASICO"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return make_response(ans[0],200)
#
#clase que retorna todo el programa de optativas de una carrera
class ProgramaOptativas(Resource):
    def get(self,carrera):
        pipeline=[
                {"$match":{"carrera":carrera.upper()+"-SEM-OPTATIVAS"}},
            {"$project":{"_id":0,"carrera":1,"materias":1}}
            ]
        ans=list(Plan.objects.aggregate(pipeline))
        return make_response(ans[0],200)

