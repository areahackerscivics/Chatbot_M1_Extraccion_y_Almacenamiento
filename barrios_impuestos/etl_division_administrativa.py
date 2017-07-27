# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:21:20 2017

@author: vahaval

Script para cargar los datos de la division administrativa del ayuntamiento

Almacena los barrios incluyendo el distrito al que pertenecen

"""


import csv
import config
from pymongo import MongoClient
from datetime import datetime

#Variables
#Nombre del archivo que contiene los datos de barrio
file_barrios = 'Barrios.csv'
#Nombre del archivo que contiene los datos de distritos
file_distritos = 'Distritos.csv'


#lectura de los archivos con la informacion de barrios y distritos
reader = csv.DictReader(open(file_barrios,encoding="utf8"), delimiter=';')
reader_distrito = csv.DictReader(open(file_distritos,encoding="utf8"), delimiter=';')

#conexion a la base de datos 
client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)
db = client.datos_valencia
#crear indices de claves unicas
db.barrio_impuestos.create_index(
    [("barrio_key",1), ("anio", 1)],
    unique=True
)

#definir la variable que indica el año al que pertenecen los datos de carga
anio=2016
#Recorre los datos del archivo distritos y crea un diccionario con la estructura:
#   { cod_distrito : NombreDelDistrito }
list_distritos={}
for element in reader_distrito:
    distrito = {element["coddistrit"]: element["nombre"] }
    list_distritos.update(distrito)

#Recorre los datos del archivo barrios, define la estructura: 
# { id_barrio : idBarrioDefinido
#   barrio: nombreBarrio
#   barrio_key: claveFormadaParaConsultas
#   distrito: {cod_distrito: NombreDelDistrito}
#   anio: anioDatosImpuestos
#   fecha_actualizacion: fechaCargaDatos
# }
#y los almacena en mongoDB
for elem_barrio in reader:
    #quita la columna WKT que no se almacenara    
    elem_barrio.pop("WKT")
    nom_distrito = list_distritos[elem_barrio["coddistrit"]]
    #define la estructura del objeto distrito    
    distrito = {'id_distrito': elem_barrio["coddistrit"] , 'distrito': nom_distrito, 
                'distrito_key': nom_distrito.lower().strip().replace(" ","_").replace("-","_"),
                'entidad': "distrito" }
    #crea el objeto barrio
    barrio = {'id_barrio': elem_barrio["coddistbar"],'barrio': elem_barrio["nombre"].strip(), 
              'barrio_key': elem_barrio["nombre"].lower().strip().replace(" ","_").replace("-","_"),'entidad': "barrio",
              'fecha_actualizacion': datetime.now(),'distrito': distrito, 'anio': anio}
    #almacena los datos en mongoDB
    try:
        db.barrio_impuestos.insert_one(barrio)
        barrio = {}
    except:
        print ("Error al insertar en la base de datos el barrio:" , barrio)
        