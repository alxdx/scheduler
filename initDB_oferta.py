from mongoengine import connect
from api.utils import *
from database.models import OpcionMateria, ProgramaDisponible, Plan, Materia, LugarYHora, Profesor

day = { "L":"Lunes",
        "A":"Martes",
        "M":"Miercoles",
        "J":"Jueves",
        "V":"Viernes"}

production = os.environ.get('MONGODATABASE')
local = 'mongodb://localhost/scheduler'
db = connect(host = local)

#print("connected to "+ configuration)
csvs = getDocsinDir("api/HORARIO/")
docs = getCSVs(csvs)

materias_por_nivel = {}
conta_total = 0
conta_falla = 0
for dc, name in zip(docs,csvs):
    conta_nuevas = 0
    conta_actual = 0
    for index, obj in dc.iterrows():
        obj["CLAVE"] = obj["CLAVE"].replace(" ","")
        obj["NRC"] = str(obj["NRC"])
        if obj["CLAVE"] != "":
            if not  Materia.objects(mat_id = obj["CLAVE"]):
                print("materia no encontrada en plan: {} - {}".format(obj["CLAVE"],obj["MATERIA"]))
                conta_falla += 1
            else:

                if not OpcionMateria.objects(nrc = obj["NRC"]):
                    hrinicio, hrfinal = obj["HORA"].split("-") 
                    lyh = []
                    for d in obj["DIA"]:
                        l = LugarYHora(dia = day[d], hora_inicio = int(hrinicio), hora_final = int(hrfinal), salon = obj["SALON"])
                        lyh.append(l)
                    Profesor.objects(nombre = obj["PROFESOR"]).update(upsert = True,nombre = obj["PROFESOR"])
                    prof = Profesor.objects.get(nombre = obj["PROFESOR"])

                    OpcionMateria( 
                            nrc = obj["NRC"],
                            mat_id = obj["CLAVE"],
                            asignatura = obj["MATERIA"],
                            lugar_y_hora = lyh,
                            profesor = prof
                            ).save()
                    print("agregada {}".format(obj["MATERIA"]))
                    conta_nuevas += 1
                    conta_total += 1
                    pipeline = [
                            {"$match":{"materias.mat_id":obj["CLAVE"]}},
                            {"$project":{"materias":0, "_id":0}}
                            ]
                    ans = list(Plan.objects().aggregate(pipeline))[0]
                    if ans["carrera"] in materias_por_nivel:
                        materias_por_nivel[ans["carrera"]].append(obj["NRC"])
                    else:
                        materias_por_nivel[ans["carrera"]] = [obj["NRC"]]
                else:
                    om = OpcionMateria.objects.get(nrc = obj["NRC"])
                    hrinicio, hrfinal = obj["HORA"].split("-") 
                    lyh = om.lugar_y_hora
                    for d in obj["DIA"]:
                        l = LugarYHora(dia = day[d], hora_inicio = int(hrinicio), hora_final = int(hrfinal), salon = obj["SALON"])
                        if l not in lyh:
                            lyh.append(l)

                    om.update(lugar_y_hora = lyh)

                    print("actualizada {}".format(obj["MATERIA"]))
                    conta_actual += 1
                    conta_total += 1

    nn = name.split()[-1][:-4]
    print("Checked {} - added: {} updated: {}".format(nn,conta_nuevas,conta_actual))
for key in materias_por_nivel:
    ProgramaDisponible(carrera = key, materias = materias_por_nivel[key]).save()
    print("saved {} - {}".format(key,len(materias_por_nivel[key])))

print("Succesfull: {} Failed: {}".format(conta_total,conta_falla))


