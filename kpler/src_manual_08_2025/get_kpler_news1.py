# vull extreure el titol, la descripcio, la data, i guardar-ho (no se si cada noticia té més informació rellevant?) i guardar-ho com abans. es a dir, una carpeta per any/mes, i en cada mes un fitxer csv amb totes les noticies del dia
import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Ruta del fitxer HTML descarregat
INPUT_HTML = "igln_kpler_2_nice.html"
OUTPUT_DIR = "news_data"

with open(INPUT_HTML, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Trobar totes les notícies
articles = soup.find_all("div", class_="insight-content-list__item-container")

news_data = []
for art in articles:
    link = art.find("a", class_="text-preview")
    if not link:
        continue

    url = link.get("href")
    title = link.find("h2").get_text(strip=True) if link.find("h2") else None
    description = link.find("p", class_="text-preview__description").get_text(strip=True) if link.find("p", class_="text-preview__description") else None
    date_text = link.find("span", class_="info__date").get_text(strip=True) if link.find("span", class_="info__date") else None
    author = link.find("div", class_="avatar secondary")
    author_initials = author.get_text(strip=True) if author else None

    # Convertir data a format YYYY-MM-DD
    pub_date = None
    if date_text:
        try:
            pub_date = datetime.strptime(date_text, "%d %b %Y").date()
        except ValueError:
            pass  # si falla, la deixem com None

    news_data.append({
        "Date": pub_date,
        "Title": title,
        "Description": description,
        "URL": url,
        "Author": author_initials,
    })

# Guardar en carpetes per any/mes/dia
for news in news_data:
    if not news["Date"]:
        continue
    year = news["Date"].year
    month = f"{news['Date'].month:02d}"
    day = f"{news['Date'].day:02d}"

    # Carpeta any/mes
    folder_path = os.path.join(OUTPUT_DIR, str(year), month)
    os.makedirs(folder_path, exist_ok=True)

    # Fitxer per dia
    file_path = os.path.join(folder_path, f"{day}.csv")

    # Afegir o crear CSV
    df_new = pd.DataFrame([news])
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(file_path, index=False, encoding="utf-8")

print("✅ Notícies processades i guardades")
