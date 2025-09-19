import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

# Aquest programa llegeix un CSV amb notícies, genera embeddings utilitzant un model preentrenat,
# calcula la similitud entre les notícies i aplica clustering per agrupar notícies similars

# === 1. Llegim CSV amb notícies ===
df = pd.read_csv("../kpler/all_news.csv")

# Combina títol i descripció en un sol text
df["content"] = df["Title"].fillna("") + ". " + df["Description"].fillna("")

# === 2. Carreguem model d'embeddings ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generem embeddings
print("🔄 Generant embeddings...")
embeddings = model.encode(df["content"].tolist(), show_progress_bar=True)

# === 3. Guardem embeddings en fitxer separat ===
np.save("embeddings.npy", embeddings)  # fitxer binari més eficient
# També podries guardar-los dins del CSV si vols (menys recomanat perquè són grans)
print("💾 Embeddings desats a 'embeddings.npy'")

# === 4. Calcular matriu de similitud (opcional, només si vols explorar) ===
similarity_matrix = cosine_similarity(embeddings)
print("\nExemple similitud notícia 0 i 1:", similarity_matrix[0, 1])

# === 5. Clustering amb DBSCAN ===
clustering = DBSCAN(eps=0.2, min_samples=6, metric="cosine").fit(embeddings)
df["cluster_id"] = clustering.labels_

# === 6. Desa resultats en CSV ===
df.to_csv("noticies_clusteritzades.csv", index=False, encoding="utf-8")

print("\n✅ Fitxer 'noticies_clusteritzades.csv' creat amb columnes:")
print(df.columns)
print("\nClusters trobats:", set(df['cluster_id']))
