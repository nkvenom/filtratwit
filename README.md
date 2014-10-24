filtratwit
==========

Utilidad de linea de comandos para filtrar y descargar twits en formato JSON

### Requisitos

* python 2.6X o superior
* pip

### Instalación

Para instalar las librerias necesarias pip install -r requirements.txt
Ir a [dev.twitter.com/apps](dev.twitter.com/apps) y crear una aplicación llenando los datos necesarios, luego copiar los datos de autenticación a auth_twitter.conf 


### Ejemplos

Filtrar los tuits de la conferencia RubyConf Argentina:

```bash
./filtratwit.py "#rubyconfar" "@rubyconfar"
```