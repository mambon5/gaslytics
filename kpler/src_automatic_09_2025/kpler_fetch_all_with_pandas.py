#!/usr/bin/env python3
import os
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from Access_token import get_token
import time
import subprocess

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
# Funció genèrica per baixar i guardar CSV
# -----------------------------
def fetch_and_save(endpoint, filename_base, params=None):
    url = f"https://api-lng.kpler.com/v1/{endpoint}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error a l'endpoint {endpoint}: {response.status_code}")
        return
    
    df = pd.read_csv(StringIO(response.text), sep=";")
    today_str = datetime.today().strftime("%Y-%m-%d")
    output_path = os.path.join(DATA_DIR, f"{filename_base}_{today_str}.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ CSV desat: {output_path}")

# -----------------------------
# Endpoints
# -----------------------------
endpoints = [
    {"endpoint": "contracts", "filename": "kpler_contracts"},
    {"endpoint": "diversions", "filename": "kpler_diversions", "params": {"size": 100000}},
    {"endpoint": "flows", "filename": "kpler_flows", "params": {
        "flowDirection": "import",
        "split": "Destination Countries",
        "granularity": "daily",
        "startDate": "2016-01-01",
        "endDate": datetime.now().strftime("%Y-%m-%d"),
        "unit": "cm",
        "withIntraCountry": "true",
        "withForecast": "true"
    }},
    {"endpoint": "installations", "filename": "kpler_installations"},
    {"endpoint": "outages", "filename": "kpler_outages"},
    {"endpoint": "inventories", "filename": "kpler_storages_inv_countries", "params_list": [
        {"split": "byCountry"},
        {"split": "byInstallation", "filename": "kpler_storages_inv_installations"}
    ]},
    {"endpoint": "trades", "filename": "kpler_trades", "params": {
        "columns": "start,end,origin_country_name,destination_country_name,initial_seller_name,final_buyer_name"
    }},
]

# -----------------------------
# Execució
# -----------------------------
for ep in endpoints:
    if "params_list" in ep:  # Alguns endpoints tenen múltiples param sets
        for pset in ep["params_list"]:
            params = {k:v for k,v in pset.items() if k != "filename"}
            fname = pset.get("filename", ep["filename"])
            fetch_and_save(ep["endpoint"], fname, params)
    else:
        fetch_and_save(ep["endpoint"], ep["filename"], ep.get("params"))

# -----------------------------
# Temps final i mida carpeta
# -----------------------------
end_time = time.time()
elapsed_seconds = end_time - start_time

# Converteix a format llegible
if elapsed_seconds < 60:
    time_str = f"{elapsed_seconds:.2f} segons"
elif elapsed_seconds < 3600:
    time_str = f"{elapsed_seconds/60:.2f} minuts"
else:
    time_str = f"{elapsed_seconds/3600:.2f} hores"

# Mida de la carpeta data (Linux)
try:
    size_bytes = int(subprocess.check_output(["du", "-sb", DATA_DIR]).split()[0])
    size_mb = size_bytes / (1024*1024)
    size_str = f"{size_mb:.2f} MB"
except Exception:
    size_str = "No s'ha pogut calcular la mida"

print(f"\n⏱ Temps total d'execució: {time_str}")
print(f"💾 Mida de la carpeta '{DATA_DIR}': {size_str}")
