# Chatbot_M1_Extraccion_y_Almacenamiento

## Descripción
Este repositorio contiene scripts para recolectar la información relacionada a temas financieros y presupuestarios del Ayuntamiento de València para almacenarlos en una base de datos Mongo. El código creado puede ser reutilizado por otro ayuntamiento si se cumple los requisitos de formatos de los archivos de entrada.

Se realizan procesos ETL (Extracción, transformación y carga) para datos de impuestos por barrios, salarios de funcionarios y para el plan de cuentas del ayuntamiento. Se leen los archivos, se cambia la estructura de los datos y se limpia los datos para guardarlos en la base de datos

## Guía de uso
### Herramientas
Python 3.6.0

LIBRERÍAS EN PYTHON
- Pymongo
- Json
- CSV
- Numpy
- BeautifulSoup

La carga de datos se ha dividido de acuerdo a la temática de datos, y cada uno tiene unos formatos para los documentos de entrada y la estructura de la base de datos de salida.

### Impuestos por barrios
Esta temática requiere de 3 scripts que deben ser ejecutados en el siguiente orden:
- 1 etl_division_administrativa.py
- 2 etl_sinonimos_barrios.py
- 3 etl_impuestos_barrrios.py
         
Primero ingresar la información de la división administrativa del ayuntamiento usando el script **etl_division_administrativa.py** que considera el ingreso de barrios y el distrito asociado.

**Entrada**: Archivo de barrios, que contiene las siguientes columnas : 


                | WKT | codbarrio  | nombre | coddistbar | coddistrit |  
 (* Si tiene la columna codbarrio y nombre el algoritmo funciona)
 
 
   Archivo de distritos
  
  
                 | WKT | coddistrit | nombre |  


**Salida**: 
Colección = barrio_impuestos

```json
{
    "_id" : "XXXXXXXXX",
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    "distrito": {
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
    "_id" : "XXXXXXXXX",
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    "distrito": {
        "entidad" : "XXXXX", 
        "distrito_key" : "XXXX"
        "id_distrito" : XXX,
        "distrito" : "XXXX"
    },
    "sinonimos": [
        "Sinonimo 1 ",
        "Sinonimo 2 ",
        "...",
        "Sinonimo N"
    ]
}
```          

Para completar la temática falta ingresar los impuestos asociados al barrio, el script **etl_impuestos_barrios.py** cumple esta función.


**Entrada**: Archivo de impuestos asignados al barrio, que contienen las siguientes columnas : 


             | id_barrio | barrio | Impuesto 1 | Impuesto 2 | ... | Impuesto N |          


**Salida**: 
Colección = barrio_impuestos

```json
{
    "_id" : "XXXXXXXXX",
    "entidad" : "XXXXXX",
    "anio" : xxxx,
    "id_barrio" : XXX,
    "barrio" : "XXXX",
    "barrio_key" : "XXXX_XXXXX",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    "distrito": {
        "entidad" : "XXXXX", 
        "distrito_key" : "XXXX"
        "id_distrito" : XXX,
        "distrito" : "XXXX"
    },
    "sinonimos" : [
        "Sinonimo 1 ",
        "Sinonimo 2 ",
        "...........",
        "Sinonimo N"
    ],
    "impuestos": {
        "periodicidad" : "XXXX",
        "entidad" : "XXXX",
        "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
        "impuesto1" : XXX.XX,
        "impuesto2" : XXX.XX,
        "........." : XXX.XX,
        "impuestoN" : XXX.XX,
    }
}
``` 


### Salarios
script = webscraping_salarios.py


Para extraer los datos de salarios se realiza web scraping en la Web del ayuntamiento. Para realizar esta acción se tiene que identificar el objeto html que contiene los datos requeridos, en este caso los datos están almacenados en una tabla por lo que usaremos las etiquetas ``` <table>, <td> y <tr>. ```


**Entrada**: URL ( La tabla HTML a extraer tiene 4 columnas)


**Salida**: 
Colección = salarios

```json
{
    "_id" : "XXXXXXXXX",
    "nombre" : "XXXXXX",
    "salario" : xx.xx,
    "sexo" : "XXXX",
    "cargo" : "XXXXXXX",
    "fecha_desde" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ"
}

```
             

### Plan de Cuentas
script = etl_plan_cuentas.py


Este script permite guardar el plan de cuentas del ayuntamiento de un archivo plano a la base de datos, considerando usar una estructura adecuada.


**Entrada**: Archivo de cuentas 

              | anio | id_plan | id_cuenta | nombre_cuenta | credito_inicial | 

La característica peculiar en los datos es que la longitud del id_cuenta, determina el nivel de la cuenta a crear.
 - id_cuenta = 1 , es una cuenta padre
 - id_cuenta = 11, subcuenta de primer nivel
 - id_cuenta = 111, subcuenta de segundo nivel
 - id_cuenta = 1111, subcuenta de segundo nivel
              

**Salida**: 
Colección = plan_cuentas


```json
{
    "_id" : "XXXXXXXXX",
    "id" : "XXXX_X_X",
    "id_cuenta" : X,
    "id_plan" : X,
    "anio" : XXXX,
    "cuenta" : "XXXXXX",
    "credito_inicial": XX.XX
    "fecha_actualizacion" : "XXXX-XX-XXTXX:XX:XX.XXXZ",
    "subcuentas" : [
         { 
           "id" : "XXXX_X_X",
           "id_cuenta" : X,
           "id_plan" : X,
           "anio" : XXXX,
           "cuenta" : "XXXXXX",
           "credito_inicial": XX.XX
         },
         {
           "id" : "XXXX_X_X",
           "id_cuenta" : X,
           "id_plan" : X,
           "anio" : XXXX,
           "cuenta" : "XXXXXX",
           "credito_inicial": XX.XX
           "subcuentas" : [
                  { 
                    "id" : "XXXX_X_X",
                    "id_cuenta" : X,
                    "id_plan" : X,
                    "anio" : XXXX,
                    "cuenta" : "XXXXXX",
                    "credito_inicial": XX.XX
                  },
                  {
                    "id" : "XXXX_X_X",
                    "id_cuenta" : X,
                    "id_plan" : X,
                    "anio" : XXXX,
                    "cuenta" : "XXXXXX",
                    "credito_inicial": XX.XX
                  }
           ]
         }
         
    ]
}

```

Script = **extraccion_presupuesto.py**

El script extrae del [portal de transparencia Valencia](http://www.valencia.es/somclars/es/#/?_k=p2po5w) el presupuesto general.

**Entrada**: presupuesto general de la pagina de transparencia


**Salida**

Colección = presupuesto
```json
{ 
  "_id" : ObjectId("xxxxxxxxxxxxxxxxxx"),
  "Provincia" : "xxxxxx",
  "presupuesto" : "xxxxxx", 
  "anio" : xxxx
}
```
## Equipo
- Autor principal:
  - [Arnau Campos](https://www.linkedin.com/in/arnau-campos-albuixech-759b23138/) | 
  
  - [Valeria Haro](https://about.me/valexharo) | @ValeriaHaro

  - [Ricardo Cancar](https://about.me/r.cancar) | 

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


