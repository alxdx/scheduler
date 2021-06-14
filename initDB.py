import pandas as pd
import os,sys
from api.utils import *
from database.models import Materia,SimpleMateria,Plan

from mongoengine import connect,get_db

production = os.environ.get('MONGODATABASE')
local = 'mongodb://localhost/scheduler'
if sys.argv[1] == "local":
    db = connect(host = local)
elif sys.argv[1] == "production":
    db = connect(host = production)
else:
    print("para ejecutar seleccione la base de datos destino {local/production}")

Materia.drop_collection()
Plan.drop_collection()
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
                    requeridas = list(map(lambda x : x.replace(' ',''),obj["Requisitos"].split(" y "))))
            #print("checking {}".format(obj["Código"]))
            if Materia.objects(mat_id = obj["Código"]).count() == 0:
                mat.save()
                print("saved {}".format(obj["Código"]))
            else:
                to_update = Materia.objects.get(mat_id = obj["Código"])
                lst = to_update.requeridas
                for x in mat.requeridas:
                    if x not in lst:
                        lst.append(x)
                #print(lst)
                to_update.update(requeridas = lst)
                print("actualizado {}".format(obj["Código"]))
            elems.append(SimpleMateria(mat_id = obj["Código"],asignatura = obj["Asignatura"]))
    nn=name.split("/")[2][5:-4]
    print("Checked {}".format(nn))
    if not Plan.objects(carrera = nn):
        Plan(carrera = nn,materias = elems).save()

print(get_db().list_collection_names())
