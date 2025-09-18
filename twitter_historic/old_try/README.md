

app de python per calcular el preu del gas (si puja o baixa) basat en tweets diaris

1. Snsscrape de python només funciona amb python11, no amb l'actual python12, s'ha de descarregar un venv amb python11 o buscar una alternativa a rascar tweets en temps real.

### Opcions per instal·lar Python 3.11
🔧 Opció 1: Afegir el PPA de deadsnakes (Ubuntu/Debian)

Aquest PPA sempre té versions noves de Python:

```
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

Després pots crear l’entorn:

```
python3.11 -m venv envi311
source envi311/bin/activate
```

Igualment no veig com descarregar twitter trends. Faré un programa que analitzi a partir d'un csv a veure quines conclusions pot treure.

## 2. Analitzar historical twitter data

Ara provarem de descarregar al kaggle i descarregar "twitter trends daily" per crear un csv amb aquestes dades i analitzar-ho en 
```
historic_tweets.py
```


## 3. Cosas que influencian el precio del gas

sentimiento:

1. noticias de trump o parecidos. Tensiones guerras geopolítica
2. noticia en korea influencia poco el precio en europa
3. economía un poco

capturar tendencias de economía, política, trump.

seguir cuentas que hablen solo del gas.

Hacer la confusion matrix.


