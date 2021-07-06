from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from database.models import Alumno, HorarioAlumno,OpcionMateria
from .recommendations import Recomendacion
from mongoengine.errors import NotUniqueError,DoesNotExist

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
        keys_dias = {"Lunes":0,"Martes":0,"Miercoles":0,"Jueves":0,"Viernes":0,"Sabado":0}
        keys_horas = {"7:00":0,"8:00":0,"9:00":0,"10:00":0,"11:00":0,"12:00":0,"13:00":0,"14:00":0,
                      "15:00":0,"16:00":0,"17:00":0,"18:00":0,"19:00":0,"20:00":0}
        alumno_id = get_jwt_identity()
        alumno = Alumno.objects.get(id=alumno_id)
        if alumno.matricula != matricula:
            return {"msg":"la matricula no corresponde con el usuario logueado"}, 401
        try:
            if alumno.horario != None:
                HorarioAlumno.objects(created_by = alumno).delete()
        except DoesNotExist:
            pass
        body = request.get_json()
        for keys in body:
            if keys not in keys_dias:
                return {"msg":"revisa el formato de tu respuesta en la documentacion. Guarda el mismo formato retornado al generar el horario "}
            else:
                for k in body[keys]:
                    if k not in keys_horas:
                        return {"msg":"revisa el formato de tu respuesta en la documentacion. Guarda el mismo formato retornado al generar el horario "}
                    else:
                        if body[keys][k] != None:
                            if "NRC" not in body[keys][k]:
                                return {"msg":"NRC no econtrado en alguna materia. Revisa el formato de tu respuesta en la documentacion. Guarda el mismo formato retornado al generar el horario "}
        reco = Recomendacion() 
        reco.set_horario(body)
        horario = HorarioAlumno(materias = reco.get_nrcs(), created_by = alumno)
        horario.save()
        alumno.update(horario = horario)
        return body,200


