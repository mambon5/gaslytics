#!/usr/bin/env python3
import os
import csv
import requests
from io import StringIO
from datetime import datetime
from Access_token import get_token
import time
import subprocess
# fa el mateix que l'altre fetch all pero sense pandas ni cap llibreria
# que no sigui estàndard de python per permetre l'execució en entorns
# amb pocs recursos com la CPU del meu servidor 
# -----------------------------
# Temps d'inici
# -----------------------------
start_time = time.time()

# -----------------------------
# Config
# -----------------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
token = get_token()

# -----------------------------
# Funció genèrica per baixar i guardar CSV diari + consolidat
# -----------------------------
def fetch_save_daily_and_consolidated(endpoint, daily_prefix, params=None):
    url = f"https://api-lng.kpler.com/v1/{endpoint}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error a l'endpoint {endpoint}: {response.status_code}")
        return
    
    # Llegim CSV del text rebut
    csv_text = response.text.strip()
    if not csv_text:
        print(f"⚠️ CSV buit per {endpoint}")
        return
    
    csv_reader = csv.reader(StringIO(csv_text), delimiter=';')
    rows = list(csv_reader)
    if not rows:
        print(f"⚠️ Sense dades per {endpoint}")
        return

    # CSV diari
    today_str = datetime.today().strftime("%Y-%m-%d")
    daily_csv_path = os.path.join(DATA_DIR, f"{daily_prefix}_{today_str}.csv")
    with open(daily_csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ CSV diari desat: {daily_csv_path}")

    # CSV consolidat
    consolidated_csv_path = os.path.join(DATA_DIR, f"{daily_prefix}.csv")

    # Llegim l'antic si existeix
    old_rows = []
    if os.path.exists(consolidated_csv_path):
        with open(consolidated_csv_path, newline='', encoding='utf-8') as f:
            old_rows = list(csv.reader(f))
    
    # Combina i treu duplicats (basat en files senceres)
    combined = old_rows + rows[1:] if old_rows else rows
    unique = []
    seen = set()
    for r in combined:
        t = tuple(r)
        if t not in seen:
            unique.append(r)
            seen.add(t)

    with open(consolidated_csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(unique)
    print(f"✅ CSV consolidat actualitzat: {consolidated_csv_path}")

# -----------------------------
# Endpoints
# -----------------------------
endpoints = [
    {"endpoint": "contracts", "prefix": "kpler_contracts"},
    {"endpoint": "diversions", "prefix": "kpler_diversions", "params": {"size": 100000}},
    {"endpoint": "flows", "prefix": "kpler_flows", "params": {
        "flowDirection": "import",
        "split": "Destination Countries",
        "granularity": "daily",
        "startDate": "2016-01-01",
        "endDate": datetime.now().strftime("%Y-%m-%d"),
        "unit": "cm",
        "withIntraCountry": "true",
        "withForecast": "true"
    }},
    {"endpoint": "installations", "prefix": "kpler_installations"},
    {"endpoint": "outages", "prefix": "kpler_outages"},
    {"endpoint": "inventories", "prefix": "kpler_storages_inv_countries", "params_list": [
        {"split": "byCountry"},
        {"split": "byInstallation", "prefix": "kpler_storages_inv_installations"}
    ]},
    {"endpoint": "trades", "prefix": "kpler_trades", "params": {
        "columns": "start,end,origin_country_name,destination_country_name,initial_seller_name,final_buyer_name"
    }},
]

# -----------------------------
# Execució
# -----------------------------
for ep in endpoints:
    if "params_list" in ep:
        for pset in ep["params_list"]:
            params = {k:v for k,v in pset.items() if k not in ["prefix"]}
            prefix = pset.get("prefix", ep["prefix"])
            fetch_save_daily_and_consolidated(ep["endpoint"], prefix, params)
    else:
        fetch_save_daily_and_consolidated(ep["endpoint"], ep["prefix"], ep.get("params"))

# -----------------------------
# Temps final i mida carpeta
# -----------------------------
end_time = time.time()
elapsed_seconds = end_time - start_time
if elapsed_seconds < 60:
    time_str = f"{elapsed_seconds:.2f} segons"
elif elapsed_seconds < 3600:
    time_str = f"{elapsed_seconds/60:.2f} minuts"
else:
    time_str = f"{elapsed_seconds/3600:.2f} hores"

try:
    size_bytes = int(subprocess.check_output(["du", "-sb", DATA_DIR]).split()[0])
    size_mb = size_bytes / (1024*1024)
    size_str = f"{size_mb:.2f} MB"
except Exception:
    size_str = "No s'ha pogut calcular la mida"

print(f"\n⏱ Temps total d'execució: {time_str}")
print(f"💾 Mida de la carpeta '{DATA_DIR}': {size_str}")
