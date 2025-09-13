from playwright.sync_api import sync_playwright
import requests

pais = "worldwide"
data = "29-11-2024"
ztime = "Europe/Madrid"

with sync_playwright() as p:
    # Obrim un navegador en mode headless (sense interfície)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Anem a la pàgina de la data i país
    url = f"https://archive.twitter-trending.com/{pais}/{data}"
    page.goto(url)
    
    # Esperem que el JS generi el q (depèn de la web, pot ser que necessiti esperar uns segons)
    page.wait_for_timeout(3000)  # espera 3 segons
    
    # Recuperem el valor de 'q' que la web assigna a window.tghjy (o l'objecte que hi hagi)
    q = page.evaluate("window.tghjy")  # substitueix tghjy si el nom és diferent
    
    print("Q generat:", q)
    
    browser.close()

# Fem la petició POST amb el q fresc
url_post = "https://archive.twitter-trending.com/tablo_request.php"
payload = {
    "country": pais,
    "date": data,
    "ztime": ztime,
    "q": q
}

r = requests.post(url_post, data=payload)
print("STATUS:", r.status_code)
print("TEXT SAMPLE:", r.text[:1000])
