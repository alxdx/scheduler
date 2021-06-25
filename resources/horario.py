from flask_restful import Resource, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.models import Alumno
from .recommendations import Recomendacion
from mongoengine import get_connection

class HorarioRecomendado(Resource):
    
    @jwt_required()
    def post(self):
        alumno_id = get_jwt_identity()
        body = request.get_json()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != body['matricula']:
            return {'msg':'la matricula no corresponde con el usuario logueado'},401
        alumno.materias_cursadas
        p = Recomendacion()
        res = p.get_recomendacion(alumno.carrera,
                            int(body["hra_inicio"].replace(":","")),
                            int(body["hra_final"].replace(":","")),
                            cursadas = alumno.materias_cursadas)
        p.print_horario()
        return res,200

            

