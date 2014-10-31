filtratwit
==========

Utilidad de linea de comandos para filtrar y descargar twits en formato JSON

### Plataformas

Funciona en Linux y en Windows a través de cygwin

### Requisitos

* python 3X 
* pip
* pythonpy (opcional): para ver como texto los tuits descargados

### Instalación

Para instalar las librerias necesarias pip install -r requirements.txt
Ir a [dev.twitter.com/apps](dev.twitter.com/apps) y crear una aplicación llenando los datos necesarios, luego copiar los datos de autenticación a auth_twitter.conf 
La versión oficial de tweepy no funciona con python3, asi que por el momento es recomendable usar este port [https://github.com/judy2k/tweepy]( https://github.com/judy2k/tweepy)

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
Para que funcione este ejemplo es necesario quitar los comentarios, si aún no funciona quitar los backslashes. Este ejemplo se implemento en el archivo top_hashtags.sh

```bash
cat rubyconfar-20141024-2335.json | \ 
py --ji -x "x['text']" | \ # la opcion --ji quiere decir que interprete la entrada como JSON 
py -x "x if '#' in x else None" | \ # Si no encuentra hashtags en el texto ignorar la linea
py -x "'\n'.join([j.lower() for j in x.split() if j.startswith('#')])" | \ #Extraer los hashtags y separarlos por cambios de linea 
py -x "''.join(ch for ch in x if ch.isalnum())" | \ # Limpiar los hashtags si caracteres no alfabeticos contiguos 
sort | uniq -c | sort -nr
```

### Scripts
* **top_hashtags.sh**: Imprime los hashtags más usados junto con el número de veces que se uso cada uno, recibe como argumento la ruta al archivo que contiene un twitt/JSON por línea.

* **top_emoticons.sh**: Imprime el top 10 de los emoticons más usados, recibe como argumento la ruta al archivo que contiene un twitt/JSON por línea.

* **most_retweeted.sh**: Imprime el top 10 de los twits mas retuiteados, recibe un argumento que es la ruta al archivo que contiene los tuits.

