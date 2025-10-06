#!/usr/bin/env python3
import os
import pandas as pd
import requests
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
# Funció genèrica per baixar i guardar CSV diari + consolidat
# -----------------------------
def fetch_save_daily_and_consolidated(endpoint, daily_prefix, params=None):
    url = f"https://api-lng.kpler.com/v1/{endpoint}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error a l'endpoint {endpoint}: {response.status_code}")
        return
    
    df_new = pd.read_csv(StringIO(response.text), sep=";")
    
    # CSV diari
    today_str = datetime.today().strftime("%Y-%m-%d")
    daily_csv_path = os.path.join(DATA_DIR, f"{daily_prefix}_{today_str}.csv")
    df_new.to_csv(daily_csv_path, index=False)
    print(f"✅ CSV diari desat: {daily_csv_path}")
    
    # CSV consolidat
    consolidated_csv_path = os.path.join(DATA_DIR, f"{daily_prefix}.csv")
    if os.path.exists(consolidated_csv_path):
        df_old = pd.read_csv(consolidated_csv_path)
        df_combined = pd.concat([df_old, df_new])
        df_combined.drop_duplicates(inplace=True)
    else:
        df_combined = df_new
    df_combined.to_csv(consolidated_csv_path, index=False)
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
