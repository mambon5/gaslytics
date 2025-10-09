
Aquí definim uns programes de python que creen la base de dades de mysql i carreguen les taules amb els csv descarregats a `data`.


# Crear base dades mysql, usuari i donar permisos:

```
CREATE DATABASE kpler CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'kpler_user'@'localhost' IDENTIFIED BY 'StrongPassword123';

GRANT ALL PRIVILEGES ON kpler.* TO 'kpler_user'@'localhost';
FLUSH PRIVILEGES;

```

# posar contrasenyes

A un fitxer d'ambient .env i instalar `pip install python-dotenv` en el virtual environment.

També hem d'instalar `pip3 install sqlalchemy`, `pip3 install pymysql`, `pip3 install cryptography`

# Instalar base de dades

## Duplicats i camps únics

Estem assumint aquests camps únics en cada taula:

| Taula (model)           | Fitxer CSV corresponent                | Camps únics (`unique_fields`)    | Comentari                                                                                                                                              |
| ----------------------- | -------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Installation**        | `kpler_installations.csv`              | `["installation"]`               | Evita duplicats amb el mateix nom d’instal·lació (⚠️ pot ser massa restrictiu, pot fallar si hi ha instal·lacions amb mateix nom en països diferents). |
| **Contract**            | `kpler_contracts.csv`                  | `["seller", "buyer", "start"]`   | Es considera el contracte únic per venedor, comprador i data d’inici.                                                                                  |
| **Diversion**           | `kpler_diversions.csv`                 | *(cap)*                          | Es carreguen totes les files, sense comprovació de duplicats.                                                                                          |
| **Flow**                | `kpler_flows.csv`                      | `["date", "country"]`            | Es considera únic per data i país.                                                                                                                     |
| **Outage**              | `kpler_outages.csv`                    | `["installation_name", "start"]` | Es considera únic per instal·lació i data d’inici.                                                                                                     |
| **StorageCountry**      | `kpler_storages_inv_countries.csv`     | `["date", "country"]`            | Un registre únic per país i data.                                                                                                                      |
| **StorageInstallation** | `kpler_storages_inv_installations.csv` | `["date", "installation"]`       | Un registre únic per instal·lació i data.                                                                                                              |
| **Trade**               | `kpler_trades.csv`                     | *(cap)*                          | Es carreguen totes les files sense comprovar duplicats.                                                                                                |
És correcte?