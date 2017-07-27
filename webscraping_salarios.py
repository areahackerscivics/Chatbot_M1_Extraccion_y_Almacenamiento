# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 17:32:01 2017

@author: vahaval

Crea la coleccion salarios que contiene los salarios brutos anuales del alcalde y sus concejales
para lo cual se realiza scraping de la URL del ayuntamiento que contiene los datos

"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import config
from pymongo import MongoClient
from datetime import datetime

#Variables
# URL para extraer datos
URL = "http://www.valencia.es/ayuntamiento/ayuntamiento.nsf/vDocumentosTituloAux/95FFD56E2D7211EFC1257D86004964FA?OpenDocument&bdOrigen=ayuntamiento%2Fayuntamiento.nsf&idapoyo=5353592E3883B9ADC12578AB0035DCF0&lang=1&nivel=2_1"
#variable que contiene la fecha desde que son validos los salarios anuales brutos a extraerse definida en un acuerdo
fecha_acuerdo='2015-07-08'

#Conexion con la base de datos
client = MongoClient("mongodb://"+config.user+ ":"+ config.password + config.url_mongodb)
db = client.datos_valencia

db.salarios.create_index(
    [("cargo",1), ("nombre", 1)],
    unique=True
)

# ******************* SCRAPING  **********************************************
# Realizamos la petición a la web
req = requests.get(URL)
# Comprobamos que la petición nos devuelve una respuesta valida
status_code = req.status_code
if status_code == 200:
    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text, "html.parser")
    n_columns = 0
    n_rows=0
    column_names = []    
    # Obtenemos la primera tabla en el documento HTML
    # En este caso, toma la unica tabla
    table = html.find_all('table')[0] #first table
    for row in table.find_all('tr'):              
        #Determinar el numero de filas
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
            #determinar el numero de columnas
                n_columns = len(td_tags)
    #Colocamos manualmente los nombres de las columnas ya que no vienen dadas en la Web
    column_names = ["sexo","nombre","cargo","salario"]
    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,index= range(0,n_rows))    
    row_marker = 0
    #Recorrdido de la tabla para extraer los datos
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            #Usamos el tratamiento usado para determinar el sexo del funcionario y almacenarlo 
            if (column.get_text() in ("D.","D","D. ")) and column_marker == 0 :
                df.iat[row_marker,column_marker] = "Hombre"
            elif (column.get_text() in ( "Dª", "Dª.")) and column_marker == 0  :
                df.iat[row_marker,column_marker] = "Mujer"
            #eliminamos el punto de unidades de mil y cambiamos la coma por punto para convertirlo en un dato numerico    
            elif column_marker == 3 :
                df.iat[row_marker,column_marker] = float(column.get_text().replace(".","").replace(",","."))
            #cambiamos el acronimo Ma por Maria para facilitar las busquedas posteriormente            
            else:
                df.iat[row_marker,column_marker] = column.get_text().replace("Mª","María")              
            column_marker += 1            
        if len(columns) > 0:
            row_marker += 1
    #agregamos columnas al diccionario de los datos inclyendo las fechas de carga y la fecha de 
    df["fecha_actualizacion"] = datetime.now()
    df["fecha_desde"] = pd.to_datetime(fecha_acuerdo)
    try:
        #insertamos los datos almacenados en el diccionario a la base de datos    
        db.salarios.insert_many(df.to_dict('records'))
    except:
        print ("ERROR - INSERTAR SALARIOS ")
else:
    print ("ERROR - ACCESO A LA WEB  %d" % status_code)