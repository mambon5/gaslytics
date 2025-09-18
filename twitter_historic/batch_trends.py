import subprocess
import os
from datetime import datetime, timedelta

# Paràmetres
pais = "worldwide"
anys = 5  # quants anys enrere vols descarregar

# Directori base on guardarem els csv
base_dir = "files/csv"

# Data final (avui)
data_final = datetime.today()
# Data inicial (fa 10 anys)
data_inici = data_final - timedelta(days=anys * 365)

# Iterem per cada dia
dia_actual = data_inici
while dia_actual <= data_final:
    # format de la data tal com espera el teu script (dd-mm-YYYY)
    data_str = dia_actual.strftime("%d-%m-%Y")

    # carpeta any/mes
    carpeta = os.path.join(base_dir, dia_actual.strftime("%Y"), dia_actual.strftime("%m"))
    os.makedirs(carpeta, exist_ok=True)

    # fitxer de sortida esperat
    nom_csv = os.path.join(carpeta, f"trends_{pais}_{data_str}.csv")

    # si ja existeix, saltem per no repetir
    if os.path.exists(nom_csv):
        print(f"⏩ Ja existeix: {nom_csv}")
    else:
        print(f"📥 Descarregant: {data_str}")
        try:
            # cridem el teu script amb la data i el pais
            subprocess.run(
                ["python3", "get_hist_trends10.py", pais, data_str, nom_csv],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error amb {data_str}: {e}")

    # següent dia
    dia_actual += timedelta(days=1)

print("✅ Procés completat!")
