from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.models import Alumno, HorarioAlumno,OpcionMateria
from .recommendations import Recomendacion

class HorarioDeAlumno(Resource):
    @jwt_required()
    def get(self,matricula):
        alumno_id = get_jwt_identity()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != matricula:
            return {"msg":"la matricula no corresponde con el usuario logueado"}, 401
        if alumno.horario == None:
            return {"msg":"aun no tienes un horario registrado"},400
        pipeline = [
                    {"$match":{"created_by":alumno.id}},
                    {"$project":{"_id":0,"materias":1}}
                ]
        nrcs = list(HorarioAlumno.objects().aggregate(pipeline))[0]["materias"] 
        pipeline = [
                {"$match":{"_id":{"$in":nrcs}}},
                {"$project":{"profesor.id":0}}
                ]
        materias = list(OpcionMateria.objects.aggregate(pipeline))
        reco = Recomendacion()
        reco.set_info_materias(materias)
        return reco.make_horario_json()

    @jwt_required()
    def post(self,matricula):
        alumno_id = get_jwt_identity()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != matricula:
            return {"msg":"la matricula no corresponde con el usuario logueado"}, 401
        if alumno.horario != None:
            HorarioAlumno.objects(created_by = alumno).delete()
        body = request.get_json()
        reco = Recomendacion() 
        reco.set_horario(body)
        horario = HorarioAlumno(materias = reco.get_nrcs(), created_by = alumno)
        horario.save()
        alumno.update(horario = horario)
        return body,200


