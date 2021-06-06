from moongoengine import connect
import os
from .database.models import OpcionMateria

class Recomendacion():
    def __init__(self):
        host = os.environ.get("MONGOLOCAL")
        connect(host = host)
    def get_recomendacion(self, hra_ini:int, hra_fin:int, max_val = 6) -> list:
        pipeline = [
                {"$match": {"lugar_y_hora":{"$eleMatch":{"hora_inicio":{"$gte":hra_ini,"$lte":hra_ini}}}}},
                {"$limit":max_val}
                ]
        return list(OpcionMateria.objects.aggregate(pipeline))

ini, fin = [int(x) for x in input().split()]

print(Recomendacion().get_recomendacion())
