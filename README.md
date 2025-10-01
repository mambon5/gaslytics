

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


## Next steps:

1. descargar todas las noticias de newsapi. Todas de los últimos 5 años. Usando tu código usando los filtros de dani. 700 por 5 días. 
2. Semantic similarity de las palabras clave.
3. Descargar las noticias de kepler.

## Per la setmana de incomunicació 26/09/2025 (4 oct '25)

fer una api que descarregui cada dia dades.

La api es diu kpler. Taula de dades amb cargaments en vaixell. 

1. Qua actualitzi les linies d'aquesta taula cada dia, perquè hi ha vaixells que encara no han arribat a port i llavors la columna està en blanc, i altres que ja han arrivat i posen a on.

2. opció 1: descarregar cada dia tota la història dels vaixells, per tenir la base de dades actualitzada. Guardar les dades dels últims 7 dies per si hi ha un error.

3. Descargar: trends, contracts, trades, inventories, diversions, installations, flows, storage, outages, 


4. Danit_florit_old/stratfor fer webscraping de los titulares y descargue noticias mismo id (sol els titulars)

5. Danit_florit_old/kpler/GAS/ hi ha 30 pdfs en totals de 30 pagines cadascun dient diferents coses de les noticies del preu del gas. Aixo a internet est aa la web de kpler > cross commodities > webinars > monthly reports > commodity geopolitics