Hacer semantic similarity entre noticias y días.

EL objectivo seria saber donde estan las noticias parecidas.

De modo que 

El modelo DBSCAN, no parece que funcione perfectamente.

Siguientes pasos para mejorar el modelo:

1. eliminar stopwords.
2. Poner preentrenado para sacar contexto a la noticia.
3. Crear y entrenar un modelo nosotros que saque el contexto.
4. Provar de fer embeddings amb un model de context de llenguatge optimitzat per finances: "yiyanghkust/ finbert-tone".
5. Posar un dropdown menu, juntar el csv de notícies amb preus de ttf, i fer que només surtin notícies amb un ttf molt gran en el gràfic.
6. també filtrar per numero de dies de major variació, eg. els 3 dies que tenen més variació.
7. Hacer el ejercicio de las películas

Observacions:

1. ttf-ret es el canvi percentual del ttf respecte el dia anterior.

Futur projecte pel 5 d'octubre:

1. Crear una API que extregui dades d'un data provider i que els guardi en una base de dades nuestra.

# How does the sentence transformer work?

Bàsicament -> s'entrena en parelles de frases similars i no similars i les mapeja a punts d'un espai n-dimensional

The SentenceTransformer("all-MiniLM-L6-v2") model works by taking text input (sentences or paragraphs) and converting it into a fixed-size numerical vector, called a sentence embedding. This embedding captures the semantic meaning of the input text. The model uses a transformer-based architecture and is trained on vast amounts of sentence-pair data to learn how to create these meaningful embeddings. During operation (inference), the model processes the input text through its transformer layers, then uses a pooling mechanism to produce a single, fixed-size output vector. 
1. Training (How it Learns):

    Self-Supervised Learning: The model is trained using a self-supervised, contrastive learning approach. 

Dataset: It was trained on a massive dataset of over a billion sentence pairs. 
Objective: The core idea is to learn to distinguish between similar and dissimilar sentence pairs. Sentences with similar meanings are mapped to nearby points in the embedding space, while dissimilar sentences are mapped to distant points. 

2. Inference (How it Works in Practice):

    Input:
    You provide the model with a sentence or a short paragraph (up to 256 tokens, or word pieces). 

Transformer Layers:
The input text is processed by the model's stacked transformer layers. 
Pooling:
The outputs from the transformer layers are then aggregated using a pooling operation, such as mean pooling, to create a single, fixed-size vector. 
Output:
This 384-dimensional vector is the sentence embedding. These embeddings are often normalized to unit length. 
Semantic Representation:
The resulting embedding is a dense numerical representation that semantically encapsulates the input text's meaning. 

3. Applications (What You Can Do With It):

    Semantic Similarity:
    You can compare the embeddings of two sentences to determine how similar their meanings are using distance metrics like cosine similarity or Euclidean distance. 

Information Retrieval & Semantic Search:
The embeddings allow for efficient searching of documents or questions based on their meaning rather than just keywords. 
Clustering:
Sentences with similar meanings will have similar embeddings and can be grouped together in clusters. 

In essence, the model acts as a "sentence-to-vector converter," providing a way to represent text numerically so that computers can understand and process the meaning of language for various downstream NLP task


# Crea el teu propi model sentence transformer:

Molt bona pregunta 👌. La resposta és sí, pots entrenar el teu propi SentenceTransformer amb parelles de frases —de fet, és un dels seus punts forts.

🧩 Com funciona l’entrenament

El framework sentence-transformers (que ja estàs fent servir) permet:

Fine-tuning d’un model existent (p.ex. all-MiniLM-L6-v2) amb les teves dades.

Entrenar des de zero (molt més costós i poc recomanat tret que tinguis milions de dades i molta potència de càlcul).

El cas habitual és el fine-tuning supervisat, on tens parelles de frases amb una etiqueta (similar / no similar, o bé un score de similitud).

🔑 Tipus de dades que pots usar

Binary labels (0/1) → ex. (frase1, frase2, similar=1).

Similarity scores (entre 0 i 1) → ex. (frase1, frase2, score=0.85).

També pots fer triplets: (anchor, positive, negative).

🛠️ Exemple bàsic de fine-tuning

```
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# 1. Model base
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Dades d’entrenament (parelles + label)
train_examples = [
    InputExample(texts=["El vaixell carrega cru", "Un petrolier transporta petroli"], label=1.0),
    InputExample(texts=["El vaixell carrega cru", "El Barça juga demà"], label=0.0),
]

# 3. DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# 4. Loss (per exemple: CosineSimilarityLoss)
train_loss = losses.CosineSimilarityLoss(model)

# 5. Entrenar (poques èpoques és suficient)
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=3,
    warmup_steps=100
)

# 6. Desa el model
model.save("my_custom_sentence_transformer")
```
Complexitat

Dades: amb uns quants milers o desenes de milers de parelles ja pots millorar el rendiment en el teu domini.

Hardware: amb una GPU (p.ex. colab, RTX 3060, etc.) és factible; entrenar des de zero, en canvi, és molt car.

Codi: com veus, la llibreria ja t’ho dóna tot fet.