from flask import Response,request,make_response
from flask_restful import Resource
from database.models import Plan,Materia
#clase que retorna todo el programa academico de una carrera
#parametros que puede recibir son ITI || LCC || ICC
class ProgramaCompleto(Resource):
    def get(self,carrera):
        bas=Plan.objects.get(carrera=carrera+"-SEM-BASICO").to_json()
        frm=Plan.objects.get(carrera=carrera+"-SEM-FORMATIVO").to_json()
        opt=Plan.objects.get(carrera=carrera+"-SEM-OPTATIVAS").to_json()
        return make_response(json.dumps(ans),200)
        #return make_response(ans,200)

#clase que retorna todo el programa formativo de una carrera
#clase que retorna todo el programa formativo de una carrera
class ProgramaFormativo(Resource):
    def get(self,carrera):
        ans=Plan.objects.get(carrera=carrera+"-SEM-FORMATIVO").to_json()
        return make_response(ans,200)
#clase que retorna todo el programa basico de una carrera
class ProgramaBasico(Resource):
    def get(self,carrera):
        ans=Plan.objects.get(carrera=carrera+"-SEM-BASICO").to_json()
        return make_response(ans,200)
#
#clase que retorna todo el programa de optativas de una carrera
class ProgramaOptativas(Resource):
    def get(self,carrera):
        ans=Plan.objects.get(carrera=carrera+"-SEM-OPTATIVAS").to_json()
        return make_response(ans,200)

