import cloudscraper

# aquesta funció es una copia en python del codi ofuscat per geenrar el ct o q del fitxer java.js de la web "https://archive.twitter-trending.com/"
def calcular_ct(pais, data_str):
    """
    Calcula el paràmetre ct com fa la web.

    :param pais: nom del país en minúscules, ex: "argentina"
    :param data_str: data en format "dd-mm-yyyy"
    :return: ct com a string
    """
    # diccionari de codis de país (_0xd95dx4)
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
    
    return str(int(ct))  # retorna com a string, igual que JS


pais = "argentina"
data = "29-11-2024"
ct = calcular_ct(pais, data)
print(ct)

scraper = cloudscraper.create_scraper()
url = "https://archive.twitter-trending.com/tablo_request.php"
payload = {
    "country": pais,          # "argentina" o qualsevol país
    "date": data,             # "29-11-2024"
    "ztime": "Europe/Madrid", # zona horària
    "q": ct                   # el ct calculat
}

r = scraper.post(url, data=payload)

print("STATUS:", r.status_code)
print("HEADERS:", r.headers)
print("TEXT SAMPLE:", r.text[:1000])  # primers 1000 caràcters
