# este script hace la relacion de las materias que abren otra materia
# para poder buscar como en una lista doblemente ligada al momento de buscar materias

from mongoengine import connect
from database.models import Materia
import os
production = os.getenv("MONGODATABASE")
local = "mongodb://localhost/scheduler"
connect(host = local)

materias = []
num_no_revisadas= 0
revisadas = 0
for i,mat in enumerate(Materia.objects):
    print("{1} {0}:".format(mat.asignatura,mat.mat_id))
    if mat.requeridas[0] != "S/R" and "%" not in mat.requeridas[0] and "ásico" not in mat.requeridas[0]:
        revisadas += 1
        for req in mat.requeridas:
            print("\t",mat.asignatura,"requerido: ",req)
            visited = Materia.objects.get(mat_id = req)
            if visited not in  materias:
                if not hasattr(visited,"por_desbloquear"):
                    setattr(visited,"por_desbloquear",[mat.mat_id])
                else:
                    visited.por_desbloquear.append(mat.mat_id)
                materias.append(visited)
                print("\tcreado")
            else:
                for x in materias:
                    if x.mat_id == req:
                        x.por_desbloquear.append(mat.mat_id)
                        print("\tanexado")
    else:
        num_no_revisadas += 1

print("\nmodificadas: ")
for m in materias:
    print("- {:7} {} ".format(m.mat_id,m.asignatura))
    print("requ: {}".format(m.requeridas))
    print("abre: {}".format(m.por_desbloquear))
    m.update( por_desbloquear = m.por_desbloquear)
    print()

print("con requisitos: {}".format(revisadas))
print("         otros: {}".format(num_no_revisadas))

print("REVISION: ")
no_materias = []
con = 0
for m in Materia.objects:
    encontrado = False
    for n in materias:
        if n.asignatura == m.asignatura:
            print("{} {}".format(con,n.asignatura))
            con += 1
            encontrado = True
    if not encontrado:
        no_materias.append(m)
print("\nsin requisitos")
for i,m in enumerate(no_materias):
    print("{}_{} {}".format(i,m.mat_id,m.asignatura))
    print("\t Requeridas :{}".format(m.requeridas))
    print()
