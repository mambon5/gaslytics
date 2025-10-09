
- [Plan](#plan)
- [Vista precisa](#vista-precisa)
  - [Plan](#plan-1)
  - [Permisos pel servidor](#permisos-pel-servidor)
  - [Servei per mostrar les dades descaregades](#servei-per-mostrar-les-dades-descaregades)
  - [Virtual host en apache per fer accessible la app desde fora](#virtual-host-en-apache-per-fer-accessible-la-app-desde-fora)
  - [si el servei kpler\_fetch.service dona errors:](#si-el-servei-kpler_fetchservice-dona-errors)
  - [Error al executar la streamlit app al meu servidor de mireia 77](#error-al-executar-la-streamlit-app-al-meu-servidor-de-mireia-77)
  - [Sense pandas i numpy el servidor antic funciona](#sense-pandas-i-numpy-el-servidor-antic-funciona)
  - [visualització de les dades de kpler descarregades](#visualització-de-les-dades-de-kpler-descarregades)
- [Dades de kpler guardades:](#dades-de-kpler-guardades)

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
Type=simple
WorkingDirectory=/var/www/gaslytics/kpler/src_automatic_09_2025
ExecStart=/var/www/gaslytics/kpler/src_automatic_09_2025/venv/bin/python3 /var/www/gaslytics/kpler/src_automatic_09_2025/kpler_
fetch_all_auto.py
User=romanov
Group=romanov
Restart=on-failure

[Install]
WantedBy=multi-user.target

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

## Permisos pel servidor

Recordeu posar totes les carpetes de `/var/www/gaslytics/kpler/` i del virtual environment, amb permisos poc restrictius perquè el servei Apache les pugui obrir i executar!ç


## Servei per mostrar les dades descaregades

Farem una app amb Streamlit que permeti mostrar, navegar i descarregar els csv guardats.

Servei hauria de ser quelcom així: `kpler_show_css.service`

amb el codi:

```
[Unit]
Description=Streamlit App - Gaslytics
After=network.target

[Service]
User=romanov
WorkingDirectory=/var/www/gaslytics/kpler/src_automatic_09_2025
ExecStart=/var/www/gaslytics/kpler/src_automatic_09_2025/venv/bin/python3 -m streamlit run app.py \
  --server.headless true \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.enableCORS false \
  --server.enableXsrfProtection false
Restart=always

[Install]
WantedBy=multi-user.target
```
lu de `headless true`, es important per dir-li a streamlit que no demani el email per la terminal al executar-se la aplicació ja que això donaria error.

executar el servei:

```
sudo systemctl daemon-reload
sudo systemctl restart kpler_show_css.service
sudo systemctl status kpler_show_css.service
```
Podem dir-li al servidor que executi de forma automàtica aquest servei al fer boot, amb la instrucció:
```
sudo systemctl enable kpler_show_css.service
```


url local per veure la app: `http://localhost:8501`

## Virtual host en apache per fer accessible la app desde fora 

Farem el següent virtual host per poder conectar els visitants al router que vinguin per un domini en concret, al port local on està la app al servidor.
El fitxer està en aquesta carpeta i es diu `gaslytics_css.conf` i té el següent contigut:

```
<VirtualHost *:80>
    ServerName gaslytics.nescolam.com

    ProxyPreserveHost On
    ProxyRequests Off
    RewriteEngine On

    # WebSockets
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteRule ^/(.*) ws://localhost:8501/$1 [P,L]

    # HTTP normal
    RewriteCond %{HTTP:Upgrade} !websocket [NC]
    RewriteRule ^/(.*) http://localhost:8501/$1 [P,L]

    ProxyPassReverse / http://localhost:8501/
    <Proxy "http://localhost:8501/">
        Require all granted
    </Proxy>

    ErrorLog ${APACHE_LOG_DIR}/gaslytics_error.log
    CustomLog ${APACHE_LOG_DIR}/gaslytics_access.log combined
</VirtualHost>

```


## si el servei kpler_fetch.service dona errors:

recrear el virtual env de nou:

```
cd /var/www/gaslytics/kpler/src_automatic_09_2025
sudo rm -rf venv
sudo python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install pandas requests
```

## Error al executar la streamlit app al meu servidor de mireia 77

Error que `illegal instruction` que trobo tot el rato indica que el CPU del meu servidor és massa antic per fer correr les dependències de Streamlit. És a dir, no puc usar Streamlit. Farem una flask app millor.

Això passa perquè usem la llibreria pandas que depen de numpy i té instruccions precompliades amb C que usen el processador modern AVX que el meu pc potser no suporta.

## Sense pandas i numpy el servidor antic funciona  

Recopilació de com ha de funcionar els serveis:


## visualització de les dades de kpler descarregades
S'han de poder veure les dades de kpler aqui `http://gaslytics.nescolam.com/`


# Dades de kpler guardades:

Estem guardant aquesta informació:

| Taula                          | Descripció                                                                                              | Relacions clau                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **contracts**                  | Contractes de subministrament de LNG entre *sellers* i *buyers* (capacitat, durada, origen/destinació). | ↔️ `installations` (zones d’origen i destinació) <br>↔️ `flows` (moviments reals de gas)                                           |
| **diversions**                 | Vaixells que canvien destí o rumb en un viatge LNG.                                                     | ↔️ `installations` (ports o plantes d’origen i destí) <br>↔️ `trades` (moviment comercial original)                                |
| **flows**                      | Fluxos diaris d’LNG per país (importacions/exportacions).                                               | ↔️ `contracts` (per identificar acords que expliquen els fluxos) <br>↔️ `storages` (part dels fluxos pot acabar en emmagatzematge) |
| **installations**              | Llista de plantes i terminals LNG (import/export, país, operador, capacitat).                           | ↔️ `contracts`, `diversions`, `outages`, `storages inv installations`                                                              |
| **outages**                    | Parades planificades o no planificades de plantes LNG.                                                  | 🔗 `installation name` → `installations.installation`                                                                              |
| **storages inv countries**     | Volums totals d’emmagatzematge per país.                                                                | ↔️ `flows` (entrades/sortides de gas)                                                                                              |
| **storages inv installations** | Mateixa informació, però per instal·lació concreta.                                                     | 🔗 `installation` → `installations.installation`                                                                                   |
| **trades**                     | Moviments comercials de LNG entre països (origen/destinació).                                           | ↔️ `contracts` (si provenen d’un acord) <br>↔️ `diversions` (si un vaixell canvia de destí)                                        |


👉 En resum:
installations és el nucli físic (infraestructura),
contracts i trades són la part comercial,
flows i storages la part operativa,
diversions i outages els esdeveniments que afecten el flux normal.

per fer això farem dos arxius en python per guardar els csv en una base de dades mysql relacional. L'estructura del arbre de fitxers seria la següent:
```
gaslytics/
│
├── data/
│   ├── kpler_contracts.csv
│   ├── kpler_installations.csv
│   ├── kpler_flows.csv
│   ├── kpler_outages.csv
│   ├── kpler_trades.csv
│   ├── kpler_diversions.csv
│   └── kpler_storages_inv_installations.csv
├──database/
│   ├── models.py          # models SQLAlchemy
│   └── load_data.py       # script per carregar CSVs
```