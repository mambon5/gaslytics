import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib

# --- 1. Carreguem CSV amb notícies ---
df = pd.read_csv("noticies_clusteritzades.csv")  

# Comptar notícies per any
# --- Convertim 'Date' a datetime ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # errors="coerce" evita problemes si hi ha dates mal formades

# --- Creem columna Year i Month ---
df["Year"] = df["Date"].dt.year
counts_per_year = df['Year'].value_counts().sort_index()  # retorna Series: any -> count
subtitle_year = ", ".join([f"{year}: {count}" for year, count in counts_per_year.items()])

# Comptar notícies per cluster
counts_per_cluster = df['cluster_id'].value_counts().sort_index()  # cluster -> count
subtitle_cluster = ", ".join([f"Cluster {cluster}: {count}" for cluster, count in counts_per_cluster.items()])


# Combinar en un subtítol
subtitle = f"{subtitle_year} | {subtitle_cluster}"
print(subtitle)

# Crear títol amb subtítol
title_text = f"Mapa 3D de notícies per similitud semàntica<br><sup>{subtitle}</sup>"


# --- 2. Carreguem embeddings desats ---
embeddings = np.load("embeddings.npy")  # shape: [n, d]

# --- 3. Reduïm embeddings a 3D amb t-SNE ---
coords = TSNE(
    n_components=3,
    perplexity=30,
    random_state=42,
    metric="cosine"
).fit_transform(embeddings)

df["x"] = coords[:, 0]
df["y"] = coords[:, 1]
df["z"] = coords[:, 2]

# --- 4. Convertim dates a string YYYY-MM i ordenem categories ---
df["year_month_str"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")
categories = sorted(df["year_month_str"].unique())
df["year_month_str"] = pd.Categorical(df["year_month_str"], categories=categories, ordered=True)

df["Date_str"] = df["Date"].dt.strftime("%Y-%m-%d")

# --- 5. Generem gradient de colors groc → blau ---
cmap = matplotlib.colormaps["YlGnBu"].resampled(len(categories))
color_list = [mcolors.rgb2hex(cmap(i)) for i in range(len(categories))]
color_discrete_map = {cat: color_list[i] for i, cat in enumerate(categories)}

# --- 6. Mapa 3D interactiu ---
fig = px.scatter_3d(
    df,
    x="x", y="y", z="z",
    color="year_month_str",
    category_orders={"year_month_str": categories},
    color_discrete_map=color_discrete_map,
    hover_data={"cluster_id": True, "Date": True, "Title": False, "x": False, "y": False, "z": False},
    custom_data=["cluster_id", "Date_str","Title", "Description"],  # títol i descripció al click
    title=title_text,
    opacity=0.7
)

# --- 7. Tooltip: cluster, data, títol ---
fig.update_traces(
    marker=dict(size=5),
    hovertemplate="<b>Cluster: %{customdata[0]}</b><br><b>%{customdata[1]}</b><br>%{customdata[2]}<extra></extra>",
    hovertext=df["Date"]
)

# --- 8. Guardem HTML ---
fig.write_html("mapa_noticies_3d.html", include_plotlyjs="cdn")

print("✅ Mapa 3D creat: obre 'mapa_noticies_3d.html' al navegador")
