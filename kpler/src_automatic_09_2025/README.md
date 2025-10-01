# Plan

Crear un servei de linyx `systemd`, és a dir un fitxer `.service` i un timer `.timer` que cridi el servei cada dia a els 2 am. I el servei ha de fer dues coses:

1. Descarregar de la api de kpler totes les dades cada dia
2. Mantenir un csv històric amb dades deduplicades.

# Vista precisa

## Plan

🔹 1. Automatitzar amb systemd

El que proposes (.service + .timer) és perfecte per un servidor Linux:

myjob.service → defineix com executar el teu contracts.py (per exemple amb un virtualenv).

myjob.timer → s’encarrega de llançar el .service a les 2:00 de la matinada cada dia.

Exemple senzill:

/etc/systemd/system/contracts.service

```
[Unit]
Description=Descàrrega diària de dades Kpler

[Service]
Type=oneshot
ExecStart=/var/www/gaslytics/kpler/src_automatic_09_2025/venv/bin/python3 /var/www/gaslytics/kpler/src_automatic_09_2025/kpler_fetch_all.py
WorkingDirectory=/var/www/gaslytics/kpler/src_automatic_09_2025
StandardOutput=journal
StandardError=journal


```


/etc/systemd/system/contracts.timer
```
[Unit]
Description=Timer per executar Kpler Fetch cada dia a les 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target

```
Després:
```
sudo systemctl daemon-reload
sudo systemctl enable kpler_fetch.timer
sudo systemctl start kpler_fetch.timer
sudo systemctl status kpler_fetch.timer


```
watch logs:

```
journalctl -u kpler_fetch.service -f

```

mb això, cada dia a les 2:00am tens el CSV nou.
I amb systemctl list-timers veus quan s’executarà el següent.

🔹 2. Evitar duplicats i només fer append

Ara mateix el teu script torna a guardar totes les dades en un fitxer nou cada dia.
Tens dues opcions:

Opció A → Fitxer diferent per cada dia (com tens ara)

Avantatge: tens un històric complet diari.

Desavantatge: hi pot haver moltes dades duplicades si l’API retorna sempre tot.

Opció B → Fitxer únic que es va ampliant

Per fer això, pots carregar el CSV existent i fer append només de les files noves. Exemple:
```
import os
import pandas as pd

today_str = datetime.today().strftime("%Y-%m-%d")
output_path = "data/kpler_contracts.csv"

# nou dataframe de l'API
df_new = pd.read_csv(StringIO(response.text), sep=";")

if os.path.exists(output_path):
    df_old = pd.read_csv(output_path)
    # combinar i eliminar duplicats
    df = pd.concat([df_old, df_new]).drop_duplicates()
else:
    df = df_new

df.to_csv(output_path, index=False)
print(f"✅ Data updated to {output_path}")

```

El fitxer de python que descarrega totes les dades es diu `kpler_fetch_all_auto.py`.