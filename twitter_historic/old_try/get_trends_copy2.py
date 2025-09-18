from bs4 import BeautifulSoup
import pandas as pd
import re

html = """... enganxa aquí el teu fragment HTML ..."""
soup = BeautifulSoup(html, "html.parser")

def parse_count(s):
    if not s:
        return None
    s = s.replace(",", "").strip()
    if re.fullmatch(r"\d+", s):
        return int(s)
    m = re.match(r"^([\d\.]+)\s*([KM])$", s, re.I)
    if m:
        num = float(m.group(1))
        if m.group(2).upper() == "K":
            return int(num * 1_000)
        if m.group(2).upper() == "M":
            return int(num * 1_000_000)
    return None

rows = []

for container in soup.select("div.list-container"):
    h3 = container.find("h3", class_="title")
    timestamp = h3.get_text(strip=True)
    timestamp_epoch = h3.get("data-timestamp")

    for li in container.select("ol.trend-card__list li"):
        a = li.select_one("a.trend-link")
        count_tag = li.select_one("span.tweet-count")

        trend = a.get_text(strip=True) if a else None
        link = a["href"] if a and a.has_attr("href") else None

        # data-count prioritari, sinó text
        data_count = count_tag.get("data-count") if count_tag and count_tag.has_attr("data-count") else ""
        text_count = count_tag.get_text(strip=True) if count_tag else ""

        count = parse_count(data_count) or parse_count(text_count)

        rows.append({
            "timestamp": timestamp,
            "timestamp_epoch": timestamp_epoch,
            "trend": trend,
            "link": link,
            "tweet_count": count
        })

df = pd.DataFrame(rows, columns=["timestamp", "trend", "link", "tweet_count", "timestamp_epoch"])
# Assegura't que siguin strings i treu els parèntesis finals
df['timestamp_clean'] = df['timestamp'].astype(str).str.strip()
df['timestamp_clean'] = df['timestamp_clean'].str.replace(r"\s*\(.*\)$", "", regex=True)

# Converteix a datetime i format dia-mes-any
df['date'] = pd.to_datetime(df['timestamp_clean'], errors='coerce', utc=True).dt.strftime("%d-%m-%Y")

# Reordenem columnes
df = df[["date", "timestamp", "timestamp_epoch", "trend", "link", "tweet_count"]]

print(df.head(20))
