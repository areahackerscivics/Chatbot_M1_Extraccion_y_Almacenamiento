# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:15:39 2017

@author: vahaval

Script para cargar los datos de impuestos descritos por barrios 

Previamente ejecutar el script etl_division_administrativa.py y 
                               etl_sinonimos_barrios.py   

"""
import csv
import config
from pymongo import MongoClient
from datetime import datetime

#Variables
file_impuestos = 'informe.csv'

#conexion a la base de datos 
client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)
db = client.datos_valencia

#lectura del archivo con la informacion impuestos por barrios
reader = csv.DictReader(open(file_impuestos,encoding="utf8"), delimiter=',')
#variable que indica el año al que pertenecen los datos
anio=2016
#recorre el archivo
for row in reader:
        #elimina los espacios en blanco al inicio y fin del string 
        barrio = row["barrio"].strip()
        #crea nuevas columnas con datos estáticos que serán almacenados también
        row["periodicidad"] = "anual"
        row["entidad"] = "impuesto"
        row["fecha_actualizacion"] = datetime.now()
        for columna in reader.fieldnames[2:]:
            row[columna] = float (row[columna])
        row.pop("id_barrio")
        row.pop("barrio")
        #busca el barrio para enlazar los datos
        buscar_barrio=db.barrio_impuestos.find( { "barrio_key":  barrio.lower().replace(" ","_").replace("'","_"),"anio":anio }) 
        contador = 0
        #condicional para actuar en el caso de que sea encontrado el barrio, actualizar los datos de impuestos
        #caso contrario buscar alguna coincidencia del nombre del barrio con los sinónimos definidos         
        if buscar_barrio.count()>0:
            for element in buscar_barrio:
                db.barrio_impuestos.update_one({'barrio_key': element["barrio_key"], "anio": anio}, { '$set' : { "impuestos" : row}},True)
        else:
            barrio_sinonimo=db.barrio_impuestos.find(  { "sinonimos": { "$regex": barrio, "$options": 'i' } } ) 
            if barrio_sinonimo.count()>0:
                for element in barrio_sinonimo:
                    db.barrio_impuestos.update_one({'barrio_key':element["barrio_key"] , "anio": anio}, { '$set' : { "impuestos" : row}},True)
            else:
                print("ERROR - INSERTAR IMPUESTOS - No se encuentra", barrio)