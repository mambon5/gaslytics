# Explicació del codi:
#
# 1. Consulta l’API de Kpler.
# 2. Desa un CSV diari amb la data (data/kpler_contracts_YYYY-MM-DD.csv).
# 3. Manté un CSV consolidat (data/kpler_contracts.csv) amb totes les dades, eliminant duplicats.

#!/usr/bin/env python3
import os
import pandas as pd
import requests
from io import StringIO
from datetime import datetime
from Access_token import get_token  # assumeix que tens aquesta funció

# -----------------------------
# Configuració
# -----------------------------
API_URL = "https://api-lng.kpler.com/v1/contracts"
DATA_DIR = "data"
DAILY_CSV_TEMPLATE = "kpler_contracts_{date}.csv"
CONSOLIDATED_CSV = "kpler_contracts.csv"

os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# Obtenir dades de l'API
# -----------------------------
token = get_token()
response = requests.get(API_URL, headers={"Authorization": f"Bearer {token}"})

if response.status_code != 200:
    print(f"❌ Error al cridar l'API: {response.status_code}")
    exit(1)

df_new = pd.read_csv(StringIO(response.text), sep=";")

# -----------------------------
# Desa CSV diari
# -----------------------------
today_str = datetime.today().strftime("%Y-%m-%d")
daily_csv_path = os.path.join(DATA_DIR, DAILY_CSV_TEMPLATE.format(date=today_str))
df_new.to_csv(daily_csv_path, index=False)
print(f"✅ CSV diari desat a {daily_csv_path}")

# -----------------------------
# Actualitzar CSV consolidat
# -----------------------------
consolidated_csv_path = os.path.join(DATA_DIR, CONSOLIDATED_CSV)

if os.path.exists(consolidated_csv_path):
    df_old = pd.read_csv(consolidated_csv_path)
    df_combined = pd.concat([df_old, df_new])
    df_combined.drop_duplicates(inplace=True)
else:
    df_combined = df_new

df_combined.to_csv(consolidated_csv_path, index=False)
print(f"✅ CSV consolidat actualitzat a {consolidated_csv_path}")
