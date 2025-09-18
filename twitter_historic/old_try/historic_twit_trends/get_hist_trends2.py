import re
import cloudscraper

# 1) Crear scraper que pot saltar el challenge de Cloudflare
scraper = cloudscraper.create_scraper()

# 2) URL de la pàgina
page_url = "https://archive.twitter-trending.com/worldwide/29-11-2024"
post_url = "https://archive.twitter-trending.com/tablo_request.php"

# 3) Primer GET de la pàgina per obtenir el valor de "q"
page = scraper.get(page_url)
if page.status_code != 200:
    raise Exception(f"Error carregant la pàgina: {page.status_code}")

html = page.text
print("HTML SAMPLE:\n", html[:2000])

# 4) Buscar "q" dins del codi font (normalment és un número llarg)
match = re.search(r'name="q"\s*value="(\d+)"', html)
if not match:
    raise Exception("No s'ha pogut trobar el paràmetre q a l'HTML")

q_value = match.group(1)
print("Trobat q:", q_value)

# 5) Fer el POST amb el valor correcte de q
payload = {
    "country": "worldwide",
    "date": "29-11-2024",
    "ztime": "Europe/Madrid",
    "q": q_value
}

resp = scraper.post(post_url, data=payload)

print("STATUS:", resp.status_code)
print("HEADERS:", resp.headers)
print("TEXT SAMPLE:", resp.text[:1000])  # primers 1000 caràcters
