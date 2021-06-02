import pandas as pd
import os
from api.utils import *
from database.models import Materia,SimpleMateria,Plan

from mongoengine import connect,get_db

#configuration=os.environ.get('CONFIGURATION_INIT_DB')
host = 'mongodb://localhost/scheduler'
db = connect(host = host)

#print("connected to "+ configuration)
csvs = getDocsinDir("api/PLAN/")
docs = getCSVs(csvs)
#print(csvs)
for dc,name in zip(docs,csvs):
    elems = []
    for index,obj in dc.iterrows():
        if obj["Código"] != "-":
            obj["Código"] = obj["Código"].replace(" ","")
            if obj["HT/HP por Periodo"]=="72/20":
                obj["HT/HP por Periodo"]=72
            if obj["HT por semana"]=="-" or obj["HP por semana"]=="-" or obj["HT/HP por semana"]=="-":
                obj["HT por semana"]=-1
                obj["HP por semana"]=-1
                obj["HT/HP por semana"]=-1
            
            mat = Materia(mat_id = obj["Código"],
                    asignatura=obj["Asignatura"],hrs_periodo = obj["HT/HP por Periodo"],
                    hrs_teoria_sem = obj["HT por semana"],hrs_pract_sem = obj["HP por semana"],
                    hrs_total_sem = obj["HT/HP por semana"],creditos=obj["Creditos"],
                    requeridas = obj["Requisitos"].split(" y "))
            #print("checking {}".format(obj["Código"]))
            if not Materia.objects(mat_id = obj["Código"]):
                mat.save()
                print("saved {}".format(obj["Código"]))
            elems.append(SimpleMateria(mat_id = obj["Código"],asignatura = obj["Asignatura"]))
    nn=name.split("/")[2][5:-4]
    print("Checked {}".format(nn))
    if not Plan.objects(carrera = nn):
        Plan(carrera = nn,materias = elems).save()

print(get_db().list_collection_names())
