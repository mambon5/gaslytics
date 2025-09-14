import cloudscraper

# Funció que ja tens per calcular el ct (o q)
def calcular_ct(pais, data_str):
    codigos = {
        "algeria": 58, "argentina": 68, "australia": 52, "austria": 51,
        "bahrain": 96, "belarus": 21, "belgium": 12, "brazil": 33,
        "canada": 98, "chile": 60, "colombia": 61, "denmark": 15,
        "dominican-republic": 22, "ecuador": 17, "egypt": 7, "france": 19,
        "germany": 71, "ghana": 32, "greece": 31, "guatemala": 14,
        "india": 75, "indonesia": 11, "ireland": 16, "israel": 34,
        "italy": 72, "japan": 64, "jordan": 30, "kenya": 13,
        "korea": 90, "kuwait": 1, "latvia": 63, "lebanon": 24,
        "malaysia": 88, "mexico": 62, "netherlands": 4, "new-zealand": 85,
        "nigeria": 53, "norway": 56, "oman": 3, "pakistan": 77,
        "panama": 87, "peru": 35, "philippines": 55, "poland": 39,
        "portugal": 41, "puerto-rico": 42, "qatar": 44, "russia": 95,
        "saudi-arabia": 66, "singapore": 18, "south-africa": 91,
        "spain": 23, "sweden": 29, "switzerland": 54, "thailand": 40,
        "turkey": 65, "ukraine": 86, "united-arab-emirates": 28,
        "united-kingdom": 92, "united-states": 43, "venezuela": 50,
        "vietnam": 37, "worldwide": 91
    }

    dia, mes, anyo = [int(x) for x in data_str.split("-")]
    codigo = codigos.get(pais.lower())
    if codigo is None:
        raise ValueError(f"Codi per al país '{pais}' no trobat")
    
    ct = (((((anyo - 1999) * 36 + mes * 3 + (dia * 7 + anyo + anyo + 1)) + codigo)) * 23.5)
    return str(int(ct))

# Paràmetres
pais = "worldwide"
data = "29-11-2024"
q = calcular_ct(pais, data)

# Crear scraper que evita Cloudflare
scraper = cloudscraper.create_scraper()

# URL i payload
url = "https://archive.twitter-trending.com/tablo_request.php"
payload = {
    "country": pais,
    "date": data,
    "ztime": "Europe/Madrid",
    "q": q
}

# Fer POST
r = scraper.post(url, data=payload)

# Mostrar resultat
print("Q generat:", q)
print("STATUS:", r.status_code)
print("TEXT SAMPLE:", r.text[:1000])
