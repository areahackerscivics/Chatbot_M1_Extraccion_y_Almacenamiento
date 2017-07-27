# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:25:02 2017

@author: valeh
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:01:15 2017

@author: vahaval

Script que recibe un documento JSON del plan de cuentas 
y almacena los datos en MongoDb


"""

import json
from pymongo import MongoClient
import numpy
import config

#Variables
#Nombre del archivo que contiene las cuentas contables
file_cuentas= 'gastos.json'

#Conexion a la base de datos Mongo
client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)
db = client.datos_valencia
#crear un indice de claves unicas
db.plan_cuentas.create_index(
    [("id",1)],
    unique=True
)

#lectura del archivo con la informacion del presupuesto para cada cuenta
reader = open(file_cuentas,encoding="utf8")
json_cuentas = json.load(reader)
cuentas = numpy.array(json_cuentas[0]["data"])
#tomar el año de los datos
anio=cuentas[1][0]
cuentas_padres = []
contador = 0
#Recorrer las cuentas para almacenarlas 
for row in cuentas:
    #Creamos una variable ID formada por el año, el id_plan y el id_cuenta
    id= row[0]+"_"+row[1]+"_"+row[2]
    #Creamos un objeto cuenta con los atributos necesarios
    cuenta = {"id": id , 'id_plan': row[1] , 'id_cuenta': row[2], 'cuenta': row[3].upper(),
                'credito_inicial': float(row[4]), 'anio': int(row[0])}
    #Filtro para identificar y almacenar cuentas padre
    if len(row[2])==1:  
        try:
            db.plan_cuentas.insert_one(cuenta)
        except:
            print (cuenta)
    #Filtro para identificar y almacenar subcuentas de primer nivel
    elif len(row[2])==2:
        # Definimos el id de la cuenta padre
        id_cuenta_padre = row[0]+"_" +row[1]+"_"+row[2][0:1]
        # Buscamos la cuenta padre para asociar la subcuenta
        cuenta_padre = db.plan_cuentas.find_one( { "id": id_cuenta_padre})
        # Si no encuentra la cuenta padre, se crea una cuenta al mismo nivel 
        if cuenta_padre is None:
            cuentas_padres.append(cuenta)
        else:
            #actualiza la cuenta, agregando subcuentas
            db.plan_cuentas.update_one({'id': id_cuenta_padre}, { '$push' : { "subcuentas" : cuenta}},True)
    #Creacion de subcuentas de segundo nivel
    else:
        #Definicion de la subcuenta padre
        id_cuenta_padre= row[0]+"_" +row[1]+"_"+row[2][0:2]
        subcuenta_padre = db.plan_cuentas.find_one( { "subcuentas.id": id_cuenta_padre})
        #Filtro, si no encuentra la subcuenta crea una subcuenta de primer nivel
        if subcuenta_padre is None:
             cuentas_padres.append(cuenta)
             id_cuenta= row[0]+"_" +row[1]+"_"+row[2][0:1]
             db.plan_cuentas.update_one({'id': id_cuenta}, { '$push' : { "subcuentas" : cuenta}},True)
        #Filtro para actualizar la subcuenta de segundo nivel, agregada a la subcuenta de primer nivel
        else:
            try:
                db.plan_cuentas.update_one({'subcuentas.id': id_cuenta_padre}, { '$push' : { "subcuentas.$.subcuentas" : cuenta}}, True)
            except:
                print(id_cuenta_padre , " ERROR - ACTUALIZAR SUBCUENTA SEGUNDO NIVEL")

