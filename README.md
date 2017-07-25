# Chatbot_M1_Extraccion_y_Almacenamiento
El modulo se encarga de recolectar la información del Ayuntamiento de València y almacenarla en una base de datos MongoDB.

Se recogen datos de impuestos por barrios, salarios de funcionarios y plan de cuentas del ayuntamiento, se cambia la estructura y se limpia los datos para ser almacenados en una base de datos no estructurada(MongoDB)


#Salarios
Para extraer los datos de salarios se realiza web scraping en la Web del ayuntamiento. Para realizar esta acción se tiene que identificar el objeto html que contiene los datos requeridos, en este caso los datos están almacenados en una tabla por lo que usaremos las etiquetas <table>, <td> y <tr>. Se creo un script en python para extraer los datos de una tabla web si cambias los parámetros como la URL de extracción y la conexión a la base de datos donde se carga de datos, puedes reutilizar el código proporcionado.
