from .db import db
from flask_bcrypt import generate_password_hash,check_password_hash

class Alumno(db.Document):
    matricula=db.StringField(required=True,unique=True)
    name= db.StringField(required=True)
    mail=db.EmailField(required=True,unique=True)
    password=db.StringField(required=True)
    carrera=db.StringField(default=None)
    horario=db.ReferenceField('HorarioAlumno')
    materias_cursadas=db.ListField(db.ReferenceField('Materia'), default=[])
    last_updated=db.DateTimeField(default=None)

    def hash_password(self):
         self.password=generate_password_hash(self.password).decode('utf8')
    def check_password(self,password):
        return check_password_hash(self.password,password)

class SimpleMateria(db.EmbeddedDocument):
    mat_id=db.StringField()
    asignatura=db.StringField()

#TODO: se puede eliminar SimpleMateria y cambiar "materias" por referenceField de "Materia"
class Plan(db.Document):
    carrera=db.StringField(required=True,unique=True)
    materias=db.EmbeddedDocumentListField(SimpleMateria,required=True)

class Materia(db.Document):
    mat_id=db.StringField(primary_key=True)
    asignatura=db.StringField(required=True)
    hrs_periodo=db.IntField(required=True)
    hrs_teoria_sem=db.IntField(required=True)
    hrs_pract_sem=db.IntField(required=True)
    hrs_total_sem=db.IntField(required=True)
    creditos=db.IntField(required=True)
    requeridas=db.ListField(db.StringField())

class Profesor(db.DynamicDocument):
    nombre=db.StringField(required=True)
    #cubiculo= "CCO2 102"

class LugarYHora(db.DynamicEmbeddedDocument):
    #martes=["13:00","CCO4 301"]
    pass

class OpcionMateria(db.Document):
    nrc=db.StringField(required=True,primary_key=True)
    asignatura=db.StringField(required=True)
    lugar_y_hora=db.DynamicField(LugarYHora ,required=True)
    profesor=db.ReferenceField('Profesor')

class HorarioAlumno(db.Document):
    created_by= db.ReferenceField('Alumno',reverse_delete_rule=db.DENY)
    materias = db.ListField(db.ReferenceField('OpcionMateria'),required=True)

Alumno.register_delete_rule(HorarioAlumno,'horario',db.CASCADE)
