from mongoengine import connect,get_db
import os
from database.models import OpcionMateria,Materia,Plan
import pandas as pd
import re

class Recomendacion():

    #constructor with no arguments looks automatically for the connection of the parent instance
    #if 1 argument is passed then it stablishes a connection with the host passed
    def __init__(self,*args):

        if  len(args) == 1:
            host = os.environ.get(args[0])
            connect(host = host)

        self.info_materias = []
        self.encontradas = []
        self.dict_horario = {
            "Lunes":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None   },
            "Martes":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None   },
            "Miercoles":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None   },
            "Jueves":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None   },
            "Viernes":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None},
            "Sabado":{"7:00":None, "8:00":None,"9:00":None,"10:00":None,"11:00":None,"12:00":None,"13:00":None,"14:00":None,"15:00":None,"16:00":None,"17:00":None,"18:00":None,"19:00":None,"20:00":None   }
        }

    def show_db(self):
        print(get_db())

    def set_horario(self,horario:dict ):
        self.dict_horario = horario
    def set_info_materias(self,info_materias:list):
        self.info_materias = info_materias

    def get_nrcs(self):
        payload = []
        for dia in self.dict_horario:
            for hora in self.dict_horario[dia]:
                if self.dict_horario[dia][hora] != None:
                    if self.dict_horario[dia][hora]["NRC"] not in payload:
                        payload.append(self.dict_horario[dia][hora]["NRC"])
        return payload
        
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
                            "mat_id": {"$in":base[carrera]}}},
                {"$project":{"profesor.id":0}}
                ]
        self.info_materias = list(OpcionMateria.objects.aggregate(pipeline))
        
        return self.make_horario_json()

    def make_horario_json(self):
        
        payload = []
        for elem in self.info_materias:
            if elem["mat_id"] not in self.encontradas:
                present = False
                for d in elem["lugar_y_hora"]:
                    hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                    for h in range(0,hrs,100):
                        key = str(d["hora_inicio"]+h)
                        key = key[:-2]+":"+key[-2:]
                        if self.dict_horario[d["dia"]][key] != None:
                            present = True
                if not present:
                    self.encontradas.append(elem["mat_id"])
                    payload.append(elem)
                    for d in elem["lugar_y_hora"]:
                        hrs = d["hora_final"] - d["hora_inicio"] - 59 + 100
                        for h in range(0,hrs,100):
                            key = str(d["hora_inicio"]+h)
                            key = key[:-2]+":"+key[-2:]
                            self.dict_horario[d["dia"]][key] = {
                                "mat_id":elem["mat_id"],
                                "nombre_materia":elem["asignatura"] ,
                                "NRC":elem["_id"] ,
                                "profesor":elem["profesor"]["nombre"],
                                "hora":key,
                                "lugar":d["salon"]
                            }
        return self.dict_horario


    #This function is for testing purposes in terminal
    def print_horario(self):
        
        print(self.info_materias)
        for r in self.info_materias:
            print("{} {} {}".format(r["_id"],r["mat_id"],r["asignatura"]))
        
        print("{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}".format("HORA","Lunes","Martes","Miercoles","Jueves","Viernes\n"))
        dict_for_print = {
            "7:00": {"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "8:00": {"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "9:00": {"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "10:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "11:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "12:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "13:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "14:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "15:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "16:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "17:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "18:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "19:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None},
            "20:00":{"Lunes":None,"Martes":None,"Miercoles":None,"Jueves":None,"Viernes":None,"Sabado":None}       
        }

        for dia in self.dict_horario:
            for hora in self.dict_horario[dia]:
                if self.dict_horario[dia][hora] != None:
                    dict_for_print[hora][dia] = self.dict_horario[dia][hora] 

        for x in range(700,2100,100):
            p =str(x)+" - "+str(x+100)
            x2 = str(x)
            x2 = x2[:-2]+":"+x2[-2:]
            print("{:^20.18}{:20.18}{:20.18}{:20.18}{:20.18}{:20.18}".format(p,
                dict_for_print[x2]["Lunes"]["NRC"]+" " +dict_for_print[x2]["Lunes"]["nombre_materia"] if dict_for_print[x2]["Lunes"]!=None else "-",
                dict_for_print[x2]["Martes"]["NRC"]+" " +dict_for_print[x2]["Martes"]["nombre_materia"]if dict_for_print[x2]["Martes"]!=None else "-",
                dict_for_print[x2]["Miercoles"]["NRC"]+" " +dict_for_print[x2]["Miercoles"]["nombre_materia"]if dict_for_print[x2]["Miercoles"]!=None else "-",
                dict_for_print[x2]["Jueves"]["NRC"]+" " +dict_for_print[x2]["Jueves"]["nombre_materia"]if dict_for_print[x2]["Jueves"]!=None else "-",
                dict_for_print[x2]["Viernes"]["NRC"]+" " +dict_for_print[x2]["Viernes"]["nombre_materia"]if dict_for_print[x2]["Viernes"]!=None else "-",
                dict_for_print[x2]["Sabado"]["NRC"]+" " +dict_for_print[x2]["Sabado"]["nombre_materia"]if dict_for_print[x2]["Sabado"]!=None else "-"))


            
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

