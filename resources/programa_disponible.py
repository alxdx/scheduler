from flask import make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.models import ProgramaDisponible,OpcionMateria,Profesor
import re 
from  bson import regex 

class Programa(Resource):
    
    def valid_param(self,carrera=None,nivel=None) -> bool:
        values_carrera = ["LCC","ICC","ITI"]
        values_nivel =   ["todos","formativo","basico","optativas"]
        if carrera is not None and carrera in values_carrera:
            return True
        if nivel is not None and nivel in values_nivel:
            return True
        return False
    def get_all(self, carrera):
        reg = regex.Regex.from_native(re.compile(carrera,re.IGNORECASE))
        pipeline = [
            {"$match":{"carrera":{"$regex":reg}}},
            {"$group":{"_id":0,"materias":{"$push":"$materias"}}},
            {"$project":{
                "_id":False,
                "materias":{
                    "$reduce":{
                        "input":"$materias",
                        "initialValue":[],
                        "in":{"$concatArrays":["$$this","$$value"]}
                    }
                }
            }}]
        ans = list(ProgramaDisponible.objects.aggregate(pipeline))
        if len(ans) > 0:
            return ans[0]
        else: 
            return None
            
    def get_formativo(self,carrera):
        pipeline = [
            {"$match": {"carrera": carrera + "-SEM-FORMATIVO"}},
            {"$project": {"_id":False}}
        ]
        ans = list(ProgramaDisponible.objects.aggregate(pipeline))
        if len(ans) > 0:
            return ans[0]
        else: 
            return None

    def get_basico(self,carrera):
        pipeline = [
            {"$match": {"carrera": carrera + "-SEM-BASICO"}},
            {"$project": {"_id":False}}
        ]
        ans = list(ProgramaDisponible.objects.aggregate(pipeline))
        if len(ans) > 0:
            return ans[0]
        else: 
            return None


    def get_optativas(self,carrera):
        pipeline = [
            {"$match": {"carrera": carrera + "-SEM-OPTATIVAS"}},
            {"$project": {"_id":False}}
        ]
        ans = list(ProgramaDisponible.objects.aggregate(pipeline))
        if len(ans) > 0:
            return ans[0]
        else: 
            return None


    def get_helper(self,carrera,nivel="todos",mat_id=False,profesor=False,horarios=False,**kwargs):
        carrera = carrera.upper()
        ans = None
        if nivel == "todos" and self.valid_param(carrera = carrera) :
            ans = self.get_all(carrera)
           
        elif self.valid_param(carrera = carrera) and self.valid_param(nivel = nivel):
            if nivel == "basico":
                ans = self.get_basico(carrera)

            elif nivel == "formativo":
                ans = self.get_formativo(carrera)

            elif nivel == "optativas":
                ans = self.get_optativas(carrera)
        else:
            return None
        if ans != None:
            chooser = { "nrc":"$_id",
                        "asignatura": True
                        }
            if mat_id:
                chooser["mat_id"] = True
            if profesor:
                chooser["profesor.id"] = True
            if horarios:
                chooser["lugar_y_hora"]  = True
            ans = OpcionMateria.objects.aggregate([
                    {"$match": {"_id":{"$in":ans["materias"]}}},
                    {"$project": chooser}
                ])
            ans = list(ans)
            if profesor:
                for r in ans:
                    r["profesor"] = Profesor.objects.get(id=r["profesor"]["id"]).nombre
            for r in ans:
                for elem in r["lugar_y_hora"]:
                    elem["hora_inicio"] = str(elem["hora_inicio"])
                    elem["hora_final"] = str(elem["hora_final"])
                    elem["hora_inicio"] = elem["hora_inicio"][:-2]+":"+elem["hora_inicio"][-2:]
                    elem["hora_final"] = elem["hora_final"][:-2]+":"+elem["hora_final"][-2:]
            return {"carrera":carrera,"nivel":nivel,"materias":ans}
        else:
            return False


    @jwt_required()
    def get(self):
        ans = self.get_helper(**request.args)
        if ans != None:
            if ans:
                return make_response(ans,200)
            else:
                return make_response({"carrera":request.args.get("carrera"),"nivel":request.args.get("nivel"),"materias":"no existen materias disponibles"},200)
        else:
            return make_response({"error":"parametros de query no reconocidos"},400)
