filtratwit
==========

Utilidad de linea de comandos para filtrar y descargar twits en formato JSON

### Requisitos

* python 2.6X o superior
* pip
* pythonpy (opcional): para ver como texto los tuits descargados

### Instalación

Para instalar las librerias necesarias pip install -r requirements.txt
Ir a [dev.twitter.com/apps](dev.twitter.com/apps) y crear una aplicación llenando los datos necesarios, luego copiar los datos de autenticación a auth_twitter.conf 


### Ejemplos

Filtrar los tuits de la conferencia RubyConf Argentina:

```bash
./filtratwit.py "#rubyconfar" "@rubyconfar"
```

Filtrar los tuits de con el hashtag #angularjs que sean en español, el filtrado se hace en el lado del cliente

```bash
./filtratwit.py "#angularjs" --lang=es
```


Instalar la utilidad [pythonpy] (https://github.com/Russell91/pythonpy) que se usa con el comando py
Para revisar los resultados de proceso se pueden usar pipes y comandos estandar de UNIX


```bash
tail -n20 RubyConfAR-20141024-1601.json | head -n-1 | formatuit
```
O para monitoreo constante

```bash
watch -n5 "tail -n20 RubyConfAR-20141024-1601.json | head -n-1 | formatuit"
```

### Rankear los hashtags más usados

```bash
cat rubyconfar-20141024-2335.json | \ 
py --ji -x "x['text']" | \ 
py -x "x if '#' in x else None" | \ 
py -x "'\n'.join([j.lower() for j in x.split() if j.startswith('#')])" | \ 
py -x "''.join(ch for ch in x if ch.isalnum())" | \ 
sort | uniq -c | sort -nr
```
