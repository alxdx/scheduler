from mongoengine import connect,get_db
import os
from database.models import OpcionMateria,Materia,Plan
import pandas as pd
import re

class Recomendacion():

    #constructor with no arguments look automatically for the connection of the parent instance
    #if 1 argument is passed then  stablish a connection with the host passed
    def __init__(self,*args):
        if  len(args) == 1:
            host = os.environ.get(args[0])
            connect(host = host)
        self.res = []
        self.encontradas = []
        self.dict_horario = {
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
    def show_db(self):
        print(get_db())

    def get_recomendacion(self,carrera, hra_ini:int, hra_fin:int, max_val = 6, cursadas = [] ,requeridas = []) -> list:
        
        if max_val > 6:
            max_val = 6
        regex = {
                    "LCC":re.compile('LCC'),
                    "ITI":re.compile('ITI'),
                    "ICC":re.compile('ICC')
                }
        base = {
                "LCC":["CCOS002","CCOS003","CCOS001","FGUS001","FGUS004","FGUS002"], 
                "ICC":["ICCS001","CCOS003","CCOS001","FGUS001","FGUS004","FGUS002"],
                "ITI":["ITIS001","ITIS002","ITIS003","FGUS001","FGUS004","FGUS002","ITIS011"]
                }
        for curs in cursadas:
            if curs in base[carrera]:
                mate = Materia.objects.get(mat_id=curs)
                for c in mate.por_desbloquear:
                    if Plan.objects(__raw__={"carrera":{"$regex":regex[carrera]},"materias.mat_id":c}).count()>0:
                        base[carrera].append(c)
                base[carrera].remove(curs)

        pipeline = [
                {"$match": {"lugar_y_hora":{"$elemMatch":{"hora_inicio":{"$gte":hra_ini,"$lte":hra_fin}}},
                            "mat_id": {"$in":base[carrera]}}}
                ]
        self.res = list(OpcionMateria.objects.aggregate(pipeline))
        
        payload = []
        for elem in self.res:
            if elem["mat_id"] not in self.encontradas:
                present = False
                for d in elem["lugar_y_hora"]:
                    hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                    for h in range(0,hrs,100):
                        if self.dict_horario[d["hora_inicio"]+h][d["dia"]] != "-":
                            present = True
                if not present:
                    self.encontradas.append(elem["mat_id"])
                    payload.append(elem)
                    for d in elem["lugar_y_hora"]:
                        hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                        for h in range(0,hrs,100):
                            self.dict_horario[d["hora_inicio"]+h][d["dia"]] = elem["_id"] +" "+ elem["asignatura"]

        return payload


    def print_horario(self):
        
        print(self.res)
        for r in self.res:
            print("{} {} {}".format(r["_id"],r["mat_id"],r["asignatura"]))
        
        print("{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}".format("HORA","Lunes","Martes","Miercoles","Jueves","Viernes\n"))
        for x in range(700,2100,100):
            p =str(x)+" - "+str(x+100)
            print("{:^20.18}{:20.18}{:20.18}{:20.18}{:20.18}{:20.18}".format(p,
                self.dict_horario[x]["Lunes"],
                self.dict_horario[x]["Martes"],
                self.dict_horario[x]["Miercoles"],
                self.dict_horario[x]["Jueves"],
                self.dict_horario[x]["Viernes"]))
            
        print("materias recomendadas {}".format(len(self.encontradas)))
        print(self.encontradas)

if __name__ == "__main__":
    ini = 700
    fin = 1300
    cur = ["FGUS001","CCOS002","CCOS003"]
    ## ini, fin = [int(x) for x in input().split()]
    p = Recomendacion("MONGOLOCAL")
    res = p.get_recomendacion("LCC",ini,fin,cursadas = cur)
    p.print_horario()
    print(res)

