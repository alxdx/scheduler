from flask import Response,request,jsonify
from flask_restful import Resource
from database.models import Plan
#clase que retorna todo el programa academico de una carrera
#parametros que puede recibir son ITI || LCC || ICC
class ProgramaCompleto(Resource):
    def get(self,carrera):
        ans=[]
        bas=Plan.objects.get(carrera=carrera+"-SEM-BASICO").materias
        frm=Plan.objects.get(carrera=carrera+"-SEM-FORMATIVO").materias
        opt=Plan.objects.get(carrera=carrera+"-SEM-OPTATIVAS").materias
        for o in bas:
            ans.append(o.to_json())
        for o in frm:
            ans.append(o.to_json())
        for o in opt:
            ans.append(o.to_json())
        #print(type(bas))
        #print(ans)
        return {"carrera":carrera,"materias":ans},200
#clase que retorna todo el programa formativo de una carrera
#clase que retorna todo el programa formativo de una carrera
class ProgramaFormativo(Resource):
    pass

#clase que retorna todo el programa basico de una carrera
class ProgramaBasico(Resource):
    pass
#clase que retorna todo el programa de optativas de una carrera
class ProgramaOptativas(Resource):
    pass
