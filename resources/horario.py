from flask_restful import Resource, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.models import Alumno

class HorarioRecomendado(Resource):
    @jwt_required()
    def post(self):

        alumno_id = get_jwt_identity()
        body = request.get_json()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != body['matricula']:
            return {'msg':'la matricula no corresponde con el usuario logueado'},401


        return {"body":body['matricula']},200

            

