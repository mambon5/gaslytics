

app de python per calcular el preu del gas (si puja o baixa) basat en tweets diaris


Igualment no veig com descarregar twitter trends. Faré un programa que analitzi a partir d'un csv a veure quines conclusions pot treure.

## 2. Analitzar historical twitter data

Ara provarem de descarregar al kaggle i descarregar "twitter trends daily" per crear un csv amb aquestes dades i analitzar-ho en 
No funciona.

Approach amb èxit: el programa 
```
get_hist_trends9.py
```

renderitza la pàgina `https://archive.twitter-trending.com` en html, usant el navegador playwright, que força al javascript a imprimir-se al codi font, i no guardar-se en variables. Això ens permet 'rascar' les dades dels twitter trends més fàcilment en
la resta del codi.

El que fem és:

1. Guardar el codi font en `files/tmp`
2. Obrir el html del codi font i 'rascar' els tweeter trend names, la hora del trend, i els retweets que han tingut, i l'ordre de popularitat de cada trend.
3. Ho guardem tot en un `.csv` a `files/csv`.

El fitxer de python té per defecte un pais i dia posats a dins del codi. Es pot canviar.


## 3. Cosas que influencian el precio del gas

sentimiento:

1. noticias de trump o parecidos. Tensiones guerras geopolítica
2. noticia en korea influencia poco el precio en europa
3. economía un poco

capturar tendencias de economía, política, trump.

seguir cuentas que hablen solo del gas.

Hacer la confusion matrix.


