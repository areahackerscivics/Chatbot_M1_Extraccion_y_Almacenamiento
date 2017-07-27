# Chatbot_M1_Extraccion_y_Almacenamiento

# readme.md
## Descripción
Este repositorio contiene scripts para recolectar la información relacionada a temas financieros y presupuestarios del Ayuntamiento de València para almacenarlos en una base de datos Mongo. El código creado puede ser reutilizado por otro ayuntamiento si se cumple los requisitos de formatos de los archivos de entrada.

Se realizan procesos ETL (Extracción, transformación y carga) para datos de impuestos por barrios, salarios de funcionarios y para el plan de cuentas del ayuntamiento. Se leen los archivos, se cambia la estructura de los datos y se limpia los datos para guardarlos en la base de datos

## Guía de uso
### Herramientas
Python 3.5.2

LIBRERÍAS EN PYTHON
- Pymongo
- Json
- CSV
- Numpy
- BeautifulSoup

La carga de datos se ha dividido deacuerdo a la temática de datos, y cada uno tiene unos formatos para los documentos de entrada y la estructura de la base de datos de salida.

### Impuestos por barrios
script   1. etl_division_administrativa.py
         2. etl_sinonimos_barrios.py
         3. etl_impuestos_barrrios.py
         
Los scripts deben ejecutarse en un orden determinado, primero ingresar la información de la división administrativa del ayuntamiento que considera el ingreso de barrios y el distrito asociado.

**Entrada**: Archivo de barrios, que contiene las siguientes columnas : 
                | WKT | codbarrio  | nombre | coddistbar | coddistrit |
             (* Si tiene la columna codbarrio y nombre el algoritmo funciona)
             Archivo de distritos
                | WKT | coddistrit | nombre |
**Salida**: 
Colección = barrio_impuestos

```json
{
    "_id" : ObjectId("XXXXXXXXX"),
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    distrito: {
        "entidad" : "XXXXX", 
        "distrito_key" : "XXXX"
        "id_distrito" : XXX,
        "distrito" : "XXXX"
    }
}

```
El siguiente script a ejecutarse es **etl_sinonimos_barrios.py** , este agrega al objeto barrio un listado de sinonimos
**Entrada**: Archivo de barrios, que contiene las siguientes columnas : 
                | NombreBarrio | Sinonimo 1 | Sinonimo 2 | ... | Sinonimo N |
             (* La primera columna que contien el nombre de barrio debe ser igual al nombre del barrio ya ingresado)
             
**Salida**: 
Colección = barrio_impuestos

```json
{
    "_id" : ObjectId("XXXXXXXXX"),
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    distrito: {
        "entidad" : "XXXXX", 
        "distrito_key" : "XXXX"
        "id_distrito" : XXX,
        "distrito" : "XXXX"
    },
    **sinonimos: [
        "Sinonimo 1 ",
        "Sinonimo 2 ",
        "...",
        "Sinonimo N"
    ]**
}
```          
Para completar la temática falta ingresar los impuestos asociados al barrio, el script **etl_impuestos_barrios.py** cumple esta función.
**Entrada**: Archivo de impuestos asignados al barrio, que contienen las siguientes columnas : 
                | id_barrio | barrio | Impuesto 1 | Impuesto 2 | ... | Impuesto N |            
**Salida**: 
Colección = barrio_impuestos

```json
{
    "_id" : ObjectId("XXXXXXXXX"),
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    distrito: {
        "entidad" : "XXXXX", 
        "distrito_key" : "XXXX"
        "id_distrito" : XXX,
        "distrito" : "XXXX"
    },
    sinonimos: [
        "Sinonimo 1 ",
        "Sinonimo 2 ",
        "...",
        "Sinonimo N"
    ],
    **impuestos: {
        "periodicidad" : "XXXX",
        "entidad" : "XXXX",
        "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
        "impuesto1" : XXX.XX,
        "impuesto2" : XXX.XX,
        "........." : XXX.XX,
        "impuestoN" : XXX.XX,
    }**
}
``` 


### Salarios
script = webscraping_salarios.py

Para extraer los datos de salarios se realiza web scraping en la Web del ayuntamiento. Para realizar esta acción se tiene que identificar el objeto html que contiene los datos requeridos, en este caso los datos están almacenados en una tabla por lo que usaremos las etiquetas ```html <table>, <td> y <tr>. ```

**Entrada**: URL 
             La tabla a extraer tiene 4 columnas
**Salida**: 
Colección = salarios

```json
{
    "_id" : ObjectId("XXXXXXXXX"),
    "nombre" : "XXXXXX",
    "salario" : xx.xx,
    "sexo" : "XXXX",
    "cargo" : "XXXXXXX",
    "fecha_desde" : ISODate("XXXX-XX-XXTXX:XX:XX.XXXZ"),
    "fecha_actualizacion" : ISODate("XXXX-XX-XXTXX:XX:XX.XXXZ")
}

```
             


## Equipo
- Autor principal:
  [Arnau Campos]()
  
  [Valeria Haro](https://about.me/valexharo) | @valexharo

- Director del proyecto:

  [Diego Álvarez](https://about.me/diegoalsan) | @diegoalsan

- Codirector del proyecto:

  [David Pardo](https://about.me/david_pardo) | @davidpardo

## Contexto del proyecto

El trabajo que contiene este repositorio se ha desarrollado en el [**Àrea Hackers cívics**](http://civichackers.cc). Un espacio de trabajo colaborativo formado por [hackers cívics](http://civichackers.webs.upv.es/conocenos/que-es-una-hacker-civicoa/) que buscamos y creamos soluciones a problemas que impiden que los ciudadanos y ciudadanas podamos influir en los asuntos que nos afectan y, así, construir una sociedad más justa. En definitiva, abordamos aquellos retos que limitan, dificultan o impiden nuestro [**empoderamiento**](http://civichackers.webs.upv.es/conocenos/una-aproximacion-al-concepto-de-empoderamiento/).

El [**Àrea Hackers cívics**](http://civichackers.cc) ha sido impulsada por la [**Cátedra Govern Obert**](http://www.upv.es/contenidos/CATGO/info/). Una iniciativa surgida de la colaboración entre la Concejalía de Transparencia, Gobierno Abierto y Cooperación del Ayuntamiento de València y la [Universitat Politècnica de València](http://www.upv.es).

![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/Logo_CGO_web.png) ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/logo_AHC_web.png)

## Términos de uso

![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)El contenido de este repositorio está sujeto a la licencia [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).


