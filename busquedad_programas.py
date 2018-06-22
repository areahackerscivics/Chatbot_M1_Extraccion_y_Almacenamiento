#!/usr/bin/python
## -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np	
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.datos_valencia
db = db.programas

years = [2011,2012,2013,2014,2015,2016,2017,2018]
	
programas = ['DEUDA PÚBLICA','SERVICIOS PÚBLICOS BÁSICOS','ACTUACIONES DE PROTECCIÓN Y PROMOCIÓN SOCIAL','PRODUCCIÓN DE BIENES PÚBLICOS DE CARACTER PREFERENTE','ACTUACIONES DE CARÁCTER ECONÓMICO','ACTUACIONES DE CARÁCTER GENERAL']

tercera=['SERVICIOS SOCIALES Y PROMOCIÓN SOCIAL','FOMENTO DEL EMPLEO']
#id_cuenta_padre= str(year) +"_"+row[0][:2] #+"_" +row[1]

deudas = {}
for year in years:
  for programa in programas:
  
    deuda = db.find_one({"$and": [{"cuenta": {'$eq': programa}},  {"anio": {'$eq': year}}]})
    deudas[programa] = deuda

#subcuenta_padre = deuda.find({}, { "subcuentas.subcuentas.cuenta": 'ASISTENCIA SOCIAL PRIMARIA'})

#print(deudas['ACTUACIONES DE CARÁCTER ECONÓMICO']['subcuentas'])
  i =0
  leyenda = []
  creditos = []
  total = 0







  for  key, prog in deudas.items():
    total += float(prog['credito_inicial'])
    if key != 'ACTUACIONES DE CARÁCTER GENERAL':
      if key != 'ACTUACIONES DE CARÁCTER ECONÓMICO':
        for x in prog['subcuentas']:
           if not x['cuenta'] in tercera:
             leyenda.append(x['cuenta'])
             creditos.append(x['credito_inicial'])
         
           elif x['cuenta'] in tercera:
                for y in x['subcuentas']:
                   leyenda.append(y['cuenta'])
                   creditos.append(y['credito_inicial'])
          
      else:
        for x in prog['subcuentas']:
           if x['cuenta']== 'TRANSPORTE PÚBLICO':
               leyenda.append(x['cuenta'])
               creditos.append(x['credito_inicial'])
          

     
  i = 0
  factores = [] 
  for credito in creditos:
    factores.append("{0:.2f}M".format(float(credito)/1000000,"%.2f"))
    i+=1
  porcentaje = []

  for valor in creditos:
     valor=float(valor)
     porcentaje.append((valor/total)*100)

  color = [(0.48,0.25,0.08), (0.34, 0.28, 0.24),(1,0.13,0),(64/255,1,111/255),(28/255,204/255,20/255),(122/255,176/255,20/255),(1,229/255,0),
         (64/255,74/255,1),(20/255,79/255,204/255),(61/255,70/255,88/255),(0,216/255,1),(1,0.5,64/255)]
#color = ['CC4A14','4C583D']

  plt.rcdefaults()
  fig, ax = plt.subplots()
  i=0
  j=0
  #ax.axvline(4.5, linestyle='--', color='black', alpha = 0.5)	 
  for valor in porcentaje:
     
     ax.barh(factores[i], valor,  align='center',
          color=color[j], ecolor='black')
     print(factores[i],valor)
     i+=1
     j+=1
     if j == len(color):
        j = 0

  porcentaje = int(max(porcentaje) + 1)
  porcentaje = np.linspace(0,porcentaje,5)
  y_pos = np.arange(len(leyenda))

  #print(y_pos)

  ax.set_yticks(y_pos)
  ax.set_xticks(porcentaje)
  ax.invert_yaxis()  # labels read top-to-bottom
  ax.legend(leyenda)
  ax.set_xlabel('Porcentaje del presupuesto total invertido por programa')
  ax.set_ylabel('Gasto en Millones de Euros por programa')
  ax.set_title('Inversión en programas año {:.0f} ({:.2f}M)'.format(year, (total/1000000)))
  ax.set_axisbelow(True)
  ax.xaxis.grid(True, linestyle='--', color='#aaaaaa')
  plt.show()





