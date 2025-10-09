from sqlalchemy import (
    create_engine, Text, Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Installation(Base):
    __tablename__ = "installations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    continent = Column(String(50))
    subcontinent = Column(String(50))
    country = Column(String(50), index=True)
    port = Column(String(100))
    installation = Column(String(150), unique=True)
    installation_type = Column(String(50))
    continent_id = Column(Integer)
    subcontinent_id = Column(Integer)
    country_id = Column(Integer)
    port_id = Column(Integer)
    installation_id = Column(Integer)
    operator = Column(String(100))
    owners = Column(String(200))
    status = Column(String(50))
    lng_storage_capacity_cbm = Column(Float)
    nominal_annual_capacity_mtpa = Column(Float)
    number_trains = Column(Integer)
    number_tanks = Column(Integer)
    start_year = Column(Integer)
    startup = Column(DateTime)


# ----------------------------------------------------------
# 🧩 CONTRACTS
# ----------------------------------------------------------
class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))
    seller = Column(String(100))
    buyer = Column(String(100))
    capacity = Column(Float)
    slots = Column(Float)
    delivery = Column(String(50))
    start = Column(DateTime)
    end = Column(DateTime)
    origin_zone = Column(String(100))
    destination_zone = Column(String(100))
    UniqueConstraint("seller", "buyer", "start", name="uix_contract_unique")


# ----------------------------------------------------------
# 🚢 DIVERSIONS
# ----------------------------------------------------------
class Diversion(Base):
    __tablename__ = "diversions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vessel = Column(String(100))
    diversion_date = Column(DateTime)
    origin = Column(String(100))
    origin_date = Column(DateTime)
    diverted_from = Column(String(100))
    new_destination = Column(String(100))
    new_destination_date = Column(DateTime)
    vessel_state = Column(String(50))
    charterer = Column(String(100))



# ----------------------------------------------------------
# ⚙️ OUTAGES
# ----------------------------------------------------------
class Outage(Base):
    __tablename__ = "outages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    outage_type = Column(String(50))
    installation_name = Column(String(150))
    installation_country = Column(String(100))
    start = Column(DateTime)
    end = Column(DateTime)
    comment = Column(Text)
    installation_id = Column(Integer)



# ----------------------------------------------------------
# 🌍 FLOWS
# ----------------------------------------------------------
class Flow(Base):
    __tablename__ = "flows"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    japan = Column(Float)
    china = Column(Float)
    south_korea = Column(Float)
    india = Column(Float)
    taiwan = Column(Float)
    france = Column(Float)
    spain = Column(Float)
    united_kingdom = Column(Float)
    turkey = Column(Float)
    italy = Column(Float)
    netherlands = Column(Float)
    thailand = Column(Float)
    pakistan = Column(Float)
    belgium = Column(Float)
    kuwait = Column(Float)
    singapore_republic = Column(Float)
    indonesia = Column(Float)
    bangladesh = Column(Float)
    portugal = Column(Float)
    poland = Column(Float)
    chile = Column(Float)
    brazil = Column(Float)
    egypt = Column(Float)
    mexico = Column(Float)
    malaysia = Column(Float)
    argentina = Column(Float)
    greece = Column(Float)
    germany = Column(Float)
    lithuania = Column(Float)
    united_arab_emirates = Column(Float)
    dominican_republic = Column(Float)
    puerto_rico = Column(Float)
    jordan = Column(Float)
    united_states = Column(Float)
    jamaica = Column(Float)
    croatia = Column(Float)
    colombia = Column(Float)
    finland = Column(Float)
    canada = Column(Float)
    philippines = Column(Float)
    panama = Column(Float)
    malta = Column(Float)
    sweden = Column(Float)
    israel = Column(Float)
    hong_kong = Column(Float)
    norway = Column(Float)
    united_states_virgin_islands = Column(Float)
    el_salvador = Column(Float)
    russian_federation = Column(Float)
    vietnam = Column(Float)
    myanmar = Column(Float)
    bahrain = Column(Float)
    gibraltar = Column(Float)
    australia = Column(Float)
    senegal = Column(Float)
    cuba = Column(Float)
    denmark = Column(Float)
    papua_new_guinea = Column(Float)
    unknown = Column(Float)
    mauritania = Column(Float)
    iceland = Column(Float)
    estonia = Column(Float)
    bahamas = Column(Float)
    period_end_date = Column(DateTime)


# ----------------------------------------------------------
# 🏦 STORAGE COUNTRIES
# ----------------------------------------------------------
class StorageCountry(Base):
    __tablename__ = "storages_inv_countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    installation = Column(String(150))
    storage_volume_kwh = Column(Float)
    net_gas_flow_kwhd = Column(Float)
    cargo_kwh = Column(Float)
    capacity_kwh = Column(Float)
    capacity_utilization = Column(Float)
    heel_kwh = Column(Float)
    country = Column(String(100))
    continent = Column(String(100))
    australia = Column(Float)
    belgium = Column(Float)
    croatia = Column(Float)
    finland = Column(Float)
    france = Column(Float)
    germany = Column(Float)
    greece = Column(Float)
    italy = Column(Float)
    lithuania = Column(Float)
    netherlands = Column(Float)
    poland = Column(Float)
    portugal = Column(Float)
    russian_federation = Column(Float)
    spain = Column(Float)
    united_kingdom = Column(Float)
    united_states = Column(Float)


# ----------------------------------------------------------
# 🏗️ STORAGE INSTALLATIONS
# ----------------------------------------------------------
class StorageInstallation(Base):
    __tablename__ = "storages_inv_installations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    installation = Column(String(150))
    storage_volume_kwh = Column(Float)
    net_gas_flow_kwhd = Column(Float)
    cargo_kwh = Column(Float)
    capacity_kwh = Column(Float)
    capacity_utilization = Column(Float)
    heel_kwh = Column(Float)
    country = Column(String(100))
    continent = Column(String(100))
    alexandroupolis = Column(Float)
    aplng = Column(Float)
    barcelona = Column(Float)
    bilbao = Column(Float)
    brunsbüttel_fsru = Column(Float)
    calcasieu_pass = Column(Float)
    cameron_liqu = Column(Float)
    cartagena_esp = Column(Float)
    corpus_christi = Column(Float)
    cove_point = Column(Float)
    dragon = Column(Float)
    dunkerque = Column(Float)
    eemsenergyterminal = Column(Float)
    el_musel = Column(Float)
    elba_island_liq = Column(Float)
    fos_cavaou = Column(Float)
    fos_tonkin = Column(Float)
    freeport = Column(Float)
    gate = Column(Float)
    glng = Column(Float)
    grain = Column(Float)
    huelva = Column(Float)
    inkoo = Column(Float)
    kamchatka_sts = Column(Float)
    klaipeda = Column(Float)
    krk_lng_fsru = Column(Float)
    la_spezia = Column(Float)
    le_havre_fsru = Column(Float)
    lubmin_fsru = Column(Float)
    montoir = Column(Float)
    mugardos = Column(Float)
    mukran = Column(Float)
    murmansk_sts = Column(Float)
    piombino_lng = Column(Float)
    plaquemines = Column(Float)
    qclng = Column(Float)
    ravenna_fsru = Column(Float)
    revithoussa = Column(Float)
    rovigo = Column(Float)
    sabine_pass = Column(Float)
    sagunto = Column(Float)
    sines = Column(Float)
    south_hook = Column(Float)
    swinoujscie_lng = Column(Float)
    toscana = Column(Float)
    wilhelmshaven_gasport = Column(Float)
    zeebrugge = Column(Float)


# ----------------------------------------------------------
# 💱 TRADES
# ----------------------------------------------------------
class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_origin = Column(DateTime)
    date_destination = Column(DateTime)
    country_origin = Column(String(100))
    country_destination = Column(String(100))
    seller_origin = Column(String(255))
    buyer_destination = Column(String(1000))

