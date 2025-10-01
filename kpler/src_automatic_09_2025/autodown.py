import requests
import csv

# -----------------------------
# 1️⃣ Credencials Kpler
# -----------------------------
EMAIL = "dani.florit88@gmail.com"
PASSWORD = "daniroma1*"

# -----------------------------
# 2️⃣ Fer login per obtenir token
# -----------------------------
login_url = "https://api-lng.kpler.com/v1/login"
login_payload = {
    "email": EMAIL,
    "password": PASSWORD
}

login_response = requests.post(login_url, json=login_payload)

if login_response.status_code != 200:
    print("Error al fer login:", login_response.status_code, login_response.text)
    exit()

token = login_response.json()["token"]
print("✅ Token obtingut correctament!")

# -----------------------------
# 3️⃣ Baixar dades de Trades
# -----------------------------
trades_url = "https://api-lng.kpler.com/v1/trades"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Paràmetres opcionals (segons documentació)
params = {
    "withIntraCountry": True
}

trades_response = requests.get(trades_url, headers=headers, params=params)

if trades_response.status_code != 200:
    print("Error al baixar trades:", trades_response.status_code, trades_response.text)
    exit()

trades_data = trades_response.json()
print(f"✅ S'han baixat {len(trades_data)} trades")

# -----------------------------
# 4️⃣ Guardar dades en CSV
# -----------------------------
# Exemple: guardem només algunes columnes (canvia segons les columnes disponibles)
columns_to_save = ["id", "origin", "destination", "volume", "product"]

csv_file = "kpler_trades.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns_to_save)
    writer.writeheader()
    for trade in trades_data:
        # Escrivim només les columnes que existeixen en cada trade
        row = {col: trade.get(col, "") for col in columns_to_save}
        writer.writerow(row)

print(f"✅ Dades guardades a {csv_file}")
