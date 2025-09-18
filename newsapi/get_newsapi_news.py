import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import time # per afegir pauses entre crides


# Carrega variables del fitxer .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("API_KEY no trobada. Comprova el fitxer .env")

print("✅ API_KEY carregada correctament")

# --- keywords (mantinc les teves) ---
keywords = [
    "lng", "liquefied natural gas", "cng", "compressed natural gas", "shale gas",
    "gas supply", "gas demand", "gas imports", "gas exports", "gas prices",
    "gas storage", "gas infrastructure", "gas transportation", "gas distribution",
    "gas pipelines", "lng terminals", "lng regasification", "lng liquefaction",
    "lng shipping", "lng tankers", "lng carriers", "floating lng", "flng",
    "lng projects", "lng contracts", "lng spot market", "lng futures", "lng index",
    "lng market", "lng trade", "lng cargoes", "lng supply chain", "lng bunkering",
    "lng storage tanks", "lng offloading", "lng import terminal", "lng export terminal",
    "lng hub", "lng demand", "lng prices", "lng volatility",
    # ... (resta igual)
]

# Helper: break keywords into smaller batches within 500-character query limits
def chunk_keywords(keywords, max_chars=480):
    batches = []
    current_batch = []
    current_len = 0
    for kw in keywords:
        kw_quoted = f'"{kw}"' if ' ' in kw else kw
        add_len = len(kw_quoted) + 4
        if current_len + add_len > max_chars:
            batches.append(current_batch)
            current_batch = [kw]
            current_len = len(kw_quoted)
        else:
            current_batch.append(kw)
            current_len += add_len
    if current_batch:
        batches.append(current_batch)
    return batches

keyword_batches = chunk_keywords(keywords)

# --- Loop per dies fins a 5 anys enrere ---
end_date = datetime.today()
start_date = end_date - timedelta(days=5*365)

current_date = end_date
days_processed = 0   # comptador de dies

while current_date >= start_date:
    day_str = current_date.strftime("%Y-%m-%d")
    print(f"\n📅 Processant {day_str}...")

    articles_data = []

    for batch in keyword_batches:
        query = ' OR '.join(f'"{kw}"' if ' ' in kw else kw for kw in batch)

        params = {
            'q': query,
            'from': day_str,
            'to': day_str,
            'sortBy': 'publishedAt',
            'pageSize': 100,
            'language': 'en',
            'apiKey': API_KEY
        }

        response = requests.get('https://newsapi.org/v2/everything', params=params)

        # Evita errors si la API falla
        if response.status_code != 200:
            print(f"⚠️ Error {response.status_code} per {day_str}")
            continue

        data = response.json()

        for article in data.get('articles', []):
            title = article.get('title', '')
            description = article.get('description') or ''
            content = f"{title} {description}".lower()

            match_count = sum(1 for kw in keywords if kw.lower() in content)

            iso_date = article.get('publishedAt', '')
            readable_date = (
                datetime.fromisoformat(iso_date.rstrip("Z")).strftime("%Y-%m-%d %H:%M")
                if iso_date else None
            )

            source = article.get('source', {}).get('name', 'Unknown')
            url = article.get('url', '')
            domain = url.split("//")[-1].split("/")[0] if url else 'unknown'

            articles_data.append({
                'Date': readable_date,
                'Title': title,
                'Description': description,
                'Source': source,
                'Domain': domain,
                'Keyword Matches': match_count,
                'URL': url
            })

    # Crear DataFrame i guardar si hi ha notícies
    # Crear DataFrame
    df = pd.DataFrame(articles_data).drop_duplicates(subset=['Title'])

    if not df.empty and "Keyword Matches" in df.columns:
        df = df[df["Keyword Matches"] > 0]

        if not df.empty:
            year = current_date.strftime("%Y")
            month = current_date.strftime("%m")
            day = current_date.strftime("%d")

            folder_path = os.path.join("news_data", year, month)
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, f"{day}.csv")
            df.to_csv(file_path, index=False, encoding="utf-8-sig")

            print(f"   ✅ {len(df)} notícies desades a {file_path}")
        else:
            print("   ℹ️ Cap notícia amb keywords trobada")
    else:
        print("   ℹ️ Cap notícia retornada per aquest dia")


    if not df.empty:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")

        folder_path = os.path.join("news_data", year, month)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{day}.csv")
        df.to_csv(file_path, index=False, encoding="utf-8-sig")

        print(f"   ✅ {len(df)} notícies desades a {file_path}")
    else:
        print("   ℹ️ Cap notícia amb keywords trobada")

    # Passar al dia anterior
    current_date -= timedelta(days=1)
    days_processed += 1

    # Cada 30 dies processats → dormir 1 minut
    if days_processed % 30 == 0:
        print("😴 Pausa de seguretat: esperant 60s per no sobrecarregar la API...")
        time.sleep(60)

