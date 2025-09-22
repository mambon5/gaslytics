Hacer semantic similarity entre noticias y días.

EL objectivo seria saber donde estan las noticias parecidas.

De modo que 

El modelo DBSCAN, no parece que funcione perfectamente.

Siguientes pasos para mejorar el modelo:

1. eliminar stopwords
2. Poner preentrenado para sacar contexto a la noticia
3. Crear y entrenar un modelo nosotros que saque el contexto.
4. Provar de fer embeddings amb un model de context de llenguatge optimitzat per finances: "yiyanghkust/ finbert-tone"
5. Posar un dropdown menu, juntar el csv de notícies amb preus de ttf, i fer que només surtin notícies amb un ttf molt gran en el gràfic.
6. també filtrar per numero de dies de major variació, eg. els 3 dies que tenen més variacio

Observacions:

1. ttf-ret es el canvi percentual del ttf respecte el dia anterior.