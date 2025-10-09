from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Installation, Contract, Diversion, Flow, Outage, StorageCountry, StorageInstallation, Trade
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# Carrega el fitxer .env
load_dotenv()

# Llegir les variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Crear URL per SQLAlchemy
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATA_DIR = "../data"

engine = create_engine(DB_URL)

# Crear taules si no existeixen
print(Base.metadata.tables.keys())
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()



def safe_float(v):
    try: return float(v)
    except: return None

def safe_date(v):
    if not v: return None
    v = v.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(v, fmt)
        except:
            pass
    return None

def load_generic(model, csv_path, unique_fields=None):
    """Carrega qualsevol taula, evitant duplicats per 'unique_fields'."""
    if not os.path.exists(csv_path):
        print(f"⚠️  Fitxer no trobat: {csv_path}")
        return

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # 🧹 Normalitzar els noms de les columnes, treiem simbols extranys, convertim esapsi a _ i posem e
        # tot a minúscules
        reader.fieldnames = [
            k.lower()
             .replace(" ", "_")
             .replace("(", "")
             .replace(")", "")
             .replace(".", "")
             .replace("/", "_")
             for k in reader.fieldnames
        ]

        count_new = 0
        for row in reader:
            # Converteix strings buides a None
            clean_row = {k: (v if v.strip() != "" else None) for k, v in row.items()}
            row = clean_row
            # Evitar duplicats si s’indiquen
            if unique_fields:
                filters = []
                for uf in unique_fields:
                    attr_name = uf.lower().replace(" ", "_")
                    if attr_name in row:
                        filters.append(getattr(model, attr_name) == row[attr_name])
                exists = session.execute(select(model).where(*filters)).scalar_one_or_none()
                if exists:
                    continue

            try:
                obj = model(**row)
                session.add(obj)
                count_new += 1
            except Exception as e:
                print(f"Error fila {row}: {e}")

        session.commit()
        print(f"✅ {model.__tablename__}: {count_new} files noves carregades.")


# ------------------------------------------------------
# Carregar totes les taules
# ------------------------------------------------------
if __name__ == "__main__":
    load_generic(Installation, os.path.join(DATA_DIR, "kpler_installations.csv"), ["installation"])
    load_generic(Contract, os.path.join(DATA_DIR, "kpler_contracts.csv"), ["seller", "buyer", "start"])
    load_generic(Diversion, os.path.join(DATA_DIR, "kpler_diversions.csv"))
    load_generic(Flow, os.path.join(DATA_DIR, "kpler_flows.csv"), ["date", "country"])
    load_generic(Outage, os.path.join(DATA_DIR, "kpler_outages.csv"), ["installation_name", "start"])
    load_generic(StorageCountry, os.path.join(DATA_DIR, "kpler_storages_inv_countries.csv"), ["date", "country"])
    load_generic(StorageInstallation, os.path.join(DATA_DIR, "kpler_storages_inv_installations.csv"), ["date", "installation"])
    load_generic(Trade, os.path.join(DATA_DIR, "kpler_trades.csv"))
    print("🎉 Carrega completa.")
