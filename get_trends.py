import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la pàgina de tendències globals
url = "https://trends24.in/"

# Simular un navegador per evitar bloquejos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# Obtenir el contingut HTML
response = requests.get(url, headers=headers)
response.raise_for_status()
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

# Llistes per guardar dades
timestamps = []
trend_names = []
trend_links = []
tweet_counts = []

# Cada "list-container" conté un bloc de tendències amb un timestamp
for container in soup.select("div.list-container"):
    # Timestamp
    time = container.find("h3", class_="title")
    timestamp = time.get_text(strip=True) if time else None

    # Tendències dins d'aquest timestamp
    for li in container.select("ol.trend-card__list li"):
        name_tag = li.select_one("a.trend-link")
        count_tag = li.select_one("span.tweet-count")

        trend_name = name_tag.get_text(strip=True) if name_tag else None
        trend_link = name_tag["href"] if name_tag else None
        count = count_tag.get("data-count") if count_tag else None
        count = int(count) if count and count.isdigit() else None
        

        timestamps.append(timestamp)
        trend_names.append(trend_name)
        trend_links.append(trend_link)
        tweet_counts.append(count)

# Crear DataFrame
df = pd.DataFrame({
    "timestamp": timestamps,
    "trend": trend_names,
    "link": trend_links,
    "tweet_count": tweet_counts
})

# Assegura't que siguin strings i treu els parèntesis finals
df['timestamp_clean'] = df['timestamp'].astype(str).str.strip()
df['timestamp_clean'] = df['timestamp_clean'].str.replace(r"\s*\(.*\)$", "", regex=True)

# Converteix a datetime i format dia-mes-any
df['date'] = pd.to_datetime(df['timestamp_clean'], errors='coerce', utc=True).dt.strftime("%d-%m-%Y")



print(df.head(20))  # Mostrem els primers 20
