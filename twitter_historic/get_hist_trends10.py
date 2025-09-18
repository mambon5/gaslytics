import sys
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

# --- llegim arguments ---
pais = sys.argv[1]          # ex: worldwide
data = sys.argv[2]          # ex: 29-11-2024
nom_csv = sys.argv[3]       # ruta completa on guardar el CSV

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # posa False si vols veure què passa
    page = browser.new_page()
    
    url = f"https://archive.twitter-trending.com/{pais}/{data}"
    page.goto(url)

    # 👉 esperar que es creïn els elements de tendències
    page.wait_for_selector(".trend611")

    # guardar l'HTML ja renderitzat
    html = page.content()
    with open("files/tmp/resultat_renderitzat.html", "w", encoding="utf-8") as f:
        f.write(html)

    browser.close()

    # paresegem el html amb BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    blocs = soup.find_all("div", class_="tek_tablo")

    # llista on guardarem els resultats
    resultats = []

    for bloc in blocs:
        hora = bloc.find("div", class_="trend_baslik611").get_text(strip=True)
        files = bloc.find_all("tr", class_="tr_table")
        for fila in files:
            pos = fila.find("td", class_="sira611").get_text(strip=True)
            trend = fila.find("span", class_="word_ars").get_text(strip=True).lstrip("#")

            # mirem la següent fila germana (potser té el volum)
            fila_next = fila.find_next_sibling("tr", class_="tr_table1")
            volum_tag = fila_next.find("span", class_="volume61") if fila_next else None
            if volum_tag:
                volum_text = volum_tag.get_text(strip=True)
                # treu la paraula "tweet"
                volum_text = volum_text.replace(" tweet", "").strip()
                volum = volum_text
            else:
                volum = None

            resultats.append([hora, pos, trend, volum])

# 👉 Guardem en CSV
with open(nom_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["hora", "posicio", "trend", "volum"])  # capçaleres
    writer.writerows(resultats)

print("✅ Arxiu '" + nom_csv + "' creat amb èxit!")










