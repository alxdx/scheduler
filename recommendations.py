from mongoengine import connect,get_db
import os
from database.models import OpcionMateria,Materia,Plan
import pandas as pd
import re
class Recomendacion():
    def __init__(self):
        host = os.environ.get("MONGOLOCAL")
        connect(host = host)
        res = []
    def show_db(self):
        print(get_db())

    def get_recomendacion(self, hra_ini:int, hra_fin:int, max_val = 6, cursadas = [] ,requeridas = []) -> list:
        if max_val > 6:
            max_val = 6
        regex_lcc = re.compile('LCC')
        base_lcc = ["CCOS002","CCOS003","CCOS001","FGUS001","FGUS004","FGUS002"]
        for curs in cursadas:
            if curs in base_lcc:
                mate = Materia.objects.get(mat_id=curs)
                for c in mate.por_desbloquear:
                    if Plan.objects(__raw__={"carrera":{"$regex":regex_lcc},"materias.mat_id":c}).count()>0:
                        base_lcc.append(c)
                base_lcc.remove(curs)

        print(base_lcc)
        pipeline = [
                {"$match": {"lugar_y_hora":{"$elemMatch":{"hora_inicio":{"$gte":hra_ini,"$lte":hra_fin}}},
                            "mat_id": {"$in":base_lcc}}}
                ]
        self.res = list(OpcionMateria.objects.aggregate(pipeline))
        return self.res

    def horario(self):
        print(self.res)
        for r in self.res:
            print("{} {} {}".format(r["_id"],r["mat_id"],r["asignatura"]))

        dict_horario = {
            700: {"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            800: {"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            900: {"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1000:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1100:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1200:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1300:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1400:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1500:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1600:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1700:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1800:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            1900:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"},
            2000:{"Lunes":"-","Martes":"-","Miercoles":"-","Jueves":"-","Viernes":"-"}
        }
        encontradas = []
        for elem in self.res:
            if elem["mat_id"] not in encontradas:
                present = False
                for d in elem["lugar_y_hora"]:
                    hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                    for h in range(0,hrs,100):
                        if dict_horario[d["hora_inicio"]+h][d["dia"]] != "-":
                            present = True
                if not present:
                    encontradas.append(elem["mat_id"])
                    for d in elem["lugar_y_hora"]:
                        hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                        for h in range(0,hrs,100):
                            dict_horario[d["hora_inicio"]+h][d["dia"]] = elem["_id"] +" "+ elem["asignatura"]

        print("{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}".format("HORA","Lunes","Martes","Miercoles","Jueves","Viernes\n"))

        for x in range(700,2100,100):
            p =str(x)+" - "+str(x+100)
            print("{:^20.18}{:20.18}{:20.18}{:20.18}{:20.18}{:20.18}".format(p,
                dict_horario[x]["Lunes"],
                dict_horario[x]["Martes"],
                dict_horario[x]["Miercoles"],
                dict_horario[x]["Jueves"],
                dict_horario[x]["Viernes"]))
            
        print("materias recomendadas {}".format(len(encontradas)))
        print(encontradas)
ini = 700
fin = 1300
cur = ["FGUS001","CCOS002","CCOS003"]
## ini, fin = [int(x) for x in input().split()]
p = Recomendacion()
res = p.get_recomendacion(ini,fin,cursadas = cur)
dt = pd.json_normalize(res,'lugar_y_hora',['_id','asignatura'])
p.horario()

