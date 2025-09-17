from sentence_transformers import SentenceTransformer, util

# 1. Carreguem un model d'embeddings (hi ha molts, aquest és petit i ràpid)
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Definim el tema clau
query = "gas price"

# 3. Exemple de trends de Twitter
trends = [
    "#OPECMeeting",
    "Energy crisis",
    "Taylor Swift",
    "LNG Qatar exports",
    "Bitcoin price"
]

# 4. Convertim query i trends a vectors
query_embedding = model.encode(query, convert_to_tensor=True)
trend_embeddings = model.encode(trends, convert_to_tensor=True)

# 5. Calculem similitud cosinus
scores = util.cos_sim(query_embedding, trend_embeddings)[0]

# 6. Mostrem resultats
for trend, score in zip(trends, scores):
    print(f"{trend:20} -> {float(score):.3f}")
