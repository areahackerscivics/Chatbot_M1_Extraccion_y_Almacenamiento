#!/usr/bin/env/python
"""
Created on wed Apr 28 1:25:02 2018

@author: Ricard
"""

#datos presupestarios general..
#ayuntamiento valencia...
import requests
import datetime
from config import *
from pymongo import MongoClient



gastos = ["GASTOS DE PERSONAL", "GASTOS CORRIENTES EN BIENES Y SERVICIOS","GASTOS FINANCIEROS","TRANSFERENCIAS CORRIENTES","INVERSIONES REALES", "TRANSFERENCIAS DE CAPITAL", "ACTIVOS FINANCIEROS", "PASIVOS FINANCIEROS","FONDO DE CONTINGENCIA Y OTROS IMPREVISTOS"]

url ="http://www.valencia.es:8070/somclars/sql/datos_presupuestarios/SELECT%20g.cuenta%2Cp.descripcion%2Cg.CredIniciales%20FROM%20gastos%20g%20JOIN%20planes_detalle%20p%20ON%20g.cuenta%3Dp.codigo%20AND%20g.plan%3Dp.plan%20WHERE%20g.plan%3D1%20AND%20ejercicio%3D{}%20ORDER%20BY%20cuenta%2Cp.descripcion%20ASC"

def addComa(num):
  #need to be string to add coma
  num = str(num)
  try:
     i = num.index('.')
     num = num.replace(num[i], ',')
  except:
     i = len(num)
  
  while i > 3:
     i =i - 3
     num = num[:i] + '.' + num[i:]
  return num

client = MongoClient(url_mongodb,port)
db = client.datos_valencia 
presupuesto = db.presupuesto

def presupuesto_general():
  ## extrae los gastos y los guarda en la base de datos
  years = [2011,2012,2013,2014,2015,2016,2017,2018]
  for year in years:
   total =0
   page = requests.get(url.format(year))

   if page.status_code == 200:
   
     presupuesto_datos = page.json()
     for i in range(0, len(presupuesto_datos[0]["data"])):
        if presupuesto_datos[0]["data"][i][1] in gastos:
         #print(presupuesto_datos[0]["data"][i][1], presupuesto_datos[0]["data"][i][2] )
         total += float(presupuesto_datos[0]["data"][i][2])

     json = {"Provincia":"Valencia",
             "presupuesto":addComa(format(total,"0.2f")),
              "anio":year}
     presupuesto.insert(json)

     print("%0.2f %d" %(total,year))
        
      
  

if __name__=='__main__':
   print(presupuesto_general())
