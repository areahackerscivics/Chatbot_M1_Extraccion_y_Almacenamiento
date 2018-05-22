# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:08:03 2017

@author: vahaval

Script para insertar o actualizar los sinonimos de un barrio

Recibe un archivo de sinonimos y requiere que previamente se haya ejecutado 
el script  etl_division_administrativa.py  

"""
import csv
from pymongo import MongoClient
#import config

#Variables
#Nombre del archivo que contiene los datos
file_sinonimos = "sinonimos.csv"

#conexion a la base de datos 
#client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)
client = MongoClient('localhost',27017)
db = client.datos_valencia

#Lectura del archivo que contiene los sinónimos
reader = csv.reader(open(file_sinonimos,encoding="utf8"), delimiter=',')

#Recorre el archivo para crear objetos sinonimos que se enlacen al barrio creado previamente
for row in reader:
   key = row[0]
   #buscamos el barrio creado con anterioridad en la base de datos     
   barrio_sinonimo=db.barrio_impuestos.find( { "barrio": str(key).upper() })
   #Filtro de validación para ejecutar la actualización si encuentra el barrio o caso contrario mostrar un error
   if barrio_sinonimo.count()>0:
       for element in row[1:]:
           db.barrio_impuestos.update_one({'barrio':str(key).upper()}, { '$addToSet' : { "sinonimos" : element}},True)
   else:
       print  ("ERROR - INSERTAR SINONIMOS - Clave No Encontrado", key , element)
