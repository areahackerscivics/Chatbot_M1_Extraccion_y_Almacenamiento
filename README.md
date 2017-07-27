# Chatbot_M1_Extraccion_y_Almacenamiento

#readme.md
##Descripción
Este repositorio contiene scripts para recolectar la información relacionada a temas financieros y presupuestarios del Ayuntamiento de València y almacenarla en una base de datos MongoDB. El código creado puede adaptarse para ser reutilizado por otro ayuntamiento si se cumple los requisitos de formatos de archivos de entrada.

Se recogen datos de impuestos por barrios, salarios de funcionarios y plan de cuentas del ayuntamiento, se cambia la estructura y se limpia los datos para ser almacenados en una base de datos no estructurada(MongoDB).

##Guía de uso
La carga de datos se ha dividido deacuerdo a la temática de datos a ser tratados, y cada temática tendrá unos documentos de entrada y la estructura de la base de datos de salida.


##Equipo
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



#Salarios
Para extraer los datos de salarios se realiza web scraping en la Web del ayuntamiento. Para realizar esta acción se tiene que identificar el objeto html que contiene los datos requeridos, en este caso los datos están almacenados en una tabla por lo que usaremos las etiquetas <table>, <td> y <tr>. Se creo un script en python para extraer los datos de una tabla web si cambias los parámetros como la URL de extracción y la conexión a la base de datos donde se carga de datos, puedes reutilizar el código proporcionado.
