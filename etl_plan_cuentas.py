#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:25:02 2017

@author: valeh
"""

Script que recibe un documento JSON del plan de cuentas 
y almacena los datos en MongoDb




import json
from pymongo import MongoClient
import numpy
import requests
#import config

#Variables
#Nombre del archivo que contiene las cuentas contables
file_cuentas= 'gastos.json'

#Conexion a la base de datos Mongo
#client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)'
client = MongoClient('localhost',27017)
db = client.datos_valencia
db = db.programas
#crear un indice de claves unicas
db.create_index(
    [("id",1)],
    unique=True
)

#def addComa(num):
  #need to be string to add coma
#  num = str(num)
#  try:
#     i = num.index('.')
#     num = num.replace(num[i], ',')
#  except:
#     i = len(num)
  
#  while i > 3:
#     i =i - 3
#     num = num[:i] + '.' + num[i:]
#  return num


url ="http://www.valencia.es:8070/somclars/sql/datos_presupuestarios/SELECT%20g.cuenta%2Cp.descripcion%2Cg.CredIniciales%20FROM%20gastos%20g%20JOIN%20planes_detalle%20p%20ON%20g.cuenta%3Dp.codigo%20AND%20g.plan%3Dp.plan%20WHERE%20g.plan%3D2%20AND%20ejercicio%3D{}%20ORDER%20BY%20cuenta%2Cp.descripcion%20ASC"

years = [2011,2012,2013,2014,2015,2016,2017,2018]
for year in years:
  total =0
  page = requests.get(url.format(year))

  if page.status_code == 200:
   
    json_cuentas = page.json(encoding="uft8")
    cuentas = numpy.array(json_cuentas[0]["data"])
    #print(cuentas[1])
##si se posee el archivo json
#lectura del archivo con la informacion del presupuesto para cada cuenta
#reader = open(file_cuentas,encoding="utf8")
#json_cuentas = json.load(reader)
#cuentas = numpy.array(json_cuentas[0]["data"])
#tomar el año de los datos
    #anio=cuentas[1][0]
    cuentas_padres = []
    contador = 0
#Recorrer las cuentas para almacenarlas 

    for row in cuentas:
      #Creamos una variable ID formada por el año, el id_plan y el id_cuenta
      id= str(year) +"_"+row[0]#+"_"+row[1]
      #Creamos un objeto cuenta con los atributos necesarios
      cuenta = {"id": id , 'id_cuenta': row[0], 'cuenta': row[1].upper(),
                'credito_inicial':row[2] , 'anio': year}
      #Filtro para identificar y almacenar cuentas padre

      if len(row[0])==1:  
        try:
            db.insert_one(cuenta)
        except:
            print (cuenta)

      #Filtro para identificar y almacenar subcuentas de primer nivel
      elif len(row[0])==2:
        # Definimos el id de la cuenta padre
        id_cuenta_padre = str(year) +"_"+row[0][0]#+"_" +row[1]
        # Buscamos la cuenta padre para asociar la subcuenta
        cuenta_padre = db.find_one( { "id": id_cuenta_padre})
        # Si no encuentra la cuenta padre, se crea una cuenta al mismo nivel 
        if cuenta_padre is None:
            cuentas_padres.append(cuenta)
            #id_cuenta= row[0]+"_" +row[1]
            #db.plan_cuentas.update_one({'id': id_cuenta}, { '$push' : { "subcuentas" : cuenta}},True)
        else:
            #actualiza la cuenta, agregando subcuentas
            db.update_one({'id': id_cuenta_padre}, { '$push' : { "subcuentas" : cuenta}},True)
    #Creacion de subcuentas de segundo nivel

      else:
        #Definicion de la subcuenta padre
        id_cuenta_padre= str(year) +"_"+row[0][:2] #+"_" +row[1]
       
        subcuenta_padre = db.find_one( { "subcuentas.id": id_cuenta_padre})
       
        #Filtro, si no encuentra la subcuenta crea una subcuenta de primer nivel
        if subcuenta_padre is None:
             print(cuenta)
             cuentas_padres.append(cuenta)
             #id_cuenta= str(year) row[0]+"_" #+row[1]
             #db.update_one({'id': id_cuenta}, { '$push' : { "subcuentas" : cuenta}},True)
        #Filtro para actualizar la subcuenta de segundo nivel, agregada a la subcuenta de primer nivel
        else:
            try:
                db.update_one({'subcuentas.id': id_cuenta_padre}, { '$push' : { "subcuentas.$.subcuentas" : cuenta}}, True)
            except:
                print(id_cuenta_padre , " ERROR - ACTUALIZAR SUBCUENTA SEGUNDO NIVEL")

