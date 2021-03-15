from .db import db
from flask_bcrypt import generate_password_hash,check_password_hash
class Alumno(db.Document):
    matricula=db.StringField(required=True,unique=True)
    name= db.StringField(required=True)
    mail=db.EmailField(required=True,unique=True)
    password=db.StringField(required=True)

    def hash_password(self):
         self.password=generate_password_hash(self.password).decode('utf8')
    def check_password(self,password):
        return check_password_hash(self.password,password)

class  SimpleMateria(db.EmbeddedDocument):
    mat_id=db.StringField()
    asignatura=db.StringField()


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

