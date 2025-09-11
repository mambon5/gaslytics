import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_count(s):
    """
    Converteix cadenes tipus:
      - "96485" -> 96485
      - "96K"   -> 96000
      - "1.2M"  -> 1200000
      - "96,485" -> 96485
      - None or "" -> None
    """
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None

    # neteja chars inusuals
    s = s.replace("\xa0", "").replace(",", "").replace(" ", "")

    # si és un nombre pur
    if re.fullmatch(r"\d+", s):
        return int(s)

    # format amb K/M (p.ex. 1.2K, 96K, 3M)
    m = re.match(r"^([\d\.]+)\s*([KMkm])$", s)
    if m:
        num = float(m.group(1))
        suf = m.group(2).upper()
        if suf == "K":
            return int(round(num * 1_000))
        if suf == "M":
            return int(round(num * 1_000_000))

    # fallback: extreu el primer nombre que trobi
    m2 = re.search(r"(\d+)", s)
    if m2:
        return int(m2.group(1))

    return None

# --- Exemple del scraping robust ---
url = "https://trends24.in/"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

timestamps = []
timestamps_epoch = []
trend_names = []
trend_links = []
tweet_counts = []

for container in soup.select("div.list-container"):
    h3 = container.find("h3", class_="title")
    ts_text = h3.get_text(strip=True) if h3 else None
    ts_epoch = h3.get("data-timestamp") if h3 and h3.get("data-timestamp") else None

    for li in container.select("ol.trend-card__list li"):
        name_tag = li.select_one("a.trend-link")
        count_tag = li.select_one("span.tweet-count")
        print(count_tag)

        trend_name = name_tag.get_text(strip=True) if name_tag else None
        trend_link = name_tag["href"] if name_tag and name_tag.has_attr("href") else None

        # Prioritzar data-count (atribut), si no, utilitzar el text visible
        data_count = ""
        if count_tag and count_tag.has_attr("data-count"):
            data_count = (count_tag.get("data-count") or "").strip()

        text_count = count_tag.get_text(strip=True) if count_tag else ""

        # intenta data_count (si és numèric), sino parseja el text
        if data_count and re.fullmatch(r"\d+", data_count):
            count = int(data_count)
        else:
            # prova text_count primer (p.ex. "96K", "96K", "96,485")
            count = parse_count(text_count)
            # si no vàlid, prova també a parsejar data_count per seguretat
            if count is None and data_count:
                count = parse_count(data_count)

        timestamps.append(ts_text)
        timestamps_epoch.append(ts_epoch)
        trend_names.append(trend_name)
        trend_links.append(trend_link)
        tweet_counts.append(count)

# DataFrame
df = pd.DataFrame({
    "timestamp": timestamps,
    "timestamp_epoch": timestamps_epoch,
    "trend": trend_names,
    "link": trend_links,
    "tweet_count": tweet_counts
})

# Assegura't que siguin strings i treu els parèntesis finals
df['timestamp_clean'] = df['timestamp'].astype(str).str.strip()
df['timestamp_clean'] = df['timestamp_clean'].str.replace(r"\s*\(.*\)$", "", regex=True)

# Converteix a datetime i format dia-mes-any
df['date'] = pd.to_datetime(df['timestamp_clean'], errors='coerce', utc=True).dt.strftime("%d-%m-%Y")


print(df.head(20))
