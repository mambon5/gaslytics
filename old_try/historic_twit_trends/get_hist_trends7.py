from playwright.sync_api import sync_playwright

pais = "worldwide"
data = "29-11-2024"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # posa False per veure què passa
    page = browser.new_page()
    
    url = f"https://archive.twitter-trending.com/{pais}/{data}"
    page.goto(url)

    # 👉 esperar que es creïn els elements de tendències
    page.wait_for_selector(".trend611")

    # guardar l'HTML ja renderitzat
    html = page.content()
    with open("resultat_renderitzat.html", "w", encoding="utf-8") as f:
        f.write(html)

    # o bé extreure directament els hashtags
    trends = page.query_selector_all(".trend611")
    for t in trends:
        print(t.inner_text())

    browser.close()
