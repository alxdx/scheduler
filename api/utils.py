import pandas as pd
import os

#recibe un directorio
#retorna todos los documentos de ese directorio
def getDocsinDir(directory):
    return list(map(lambda x: directory+x,os.listdir(directory)))
#recibe una lista de nombres de documentos
#retorna un lista de dataFrames
def getCSVs(docs):
    data=[]
    for x in docs:
        data.append(pd.read_csv(x))
    return data

