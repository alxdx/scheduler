from mongoengine import connect,get_db
import os
from database.models import OpcionMateria
import pandas as pd

class Recomendacion():
    def __init__(self):
        host = os.environ.get("MONGOLOCAL")
        connect(host = host)
    def show_db(self):
        print(get_db())

    def get_recomendacion(self, hra_ini:int, hra_fin:int, max_val = 6) -> list:
        if max_val > 6:
            max_val = 6
        pipeline = [
                {"$match": {"lugar_y_hora":{"$elemMatch":{"hora_inicio":{"$gte":hra_ini,"$lte":hra_fin}}}}},
                {"$limit": max_val}
                ]
        return list(OpcionMateria.objects.aggregate(pipeline))

    def horario(self):
        print("{:^20}{:20}{:20}{:20}{:20}{:20}".format("HORA","Lunes","Martes","Miercoles","Jueves","Viernes\n"))
        for x in range(8,21):
            
            print("{0:^20}".format(str(x)+"-"+str(x+1)))

ini, fin = [int(x) for x in input().split()]

p = Recomendacion()
res = p.get_recomendacion(ini,fin)
dt = pd.json_normalize(res,'lugar_y_hora',['_id','asignatura'])
p.horario()
