from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ------------------------------------------------------
# INSTALLATIONS
# ------------------------------------------------------
class Installation(Base):
    __tablename__ = "installations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    continent = Column(String(50))
    subcontinent = Column(String(50))
    country = Column(String(50), index=True)
    port = Column(String(100))
    installation = Column(String(150), unique=True)
    installation_type = Column(String(50))
    operator = Column(String(100))
    owners = Column(String(200))
    status = Column(String(50))
    nominal_capacity_mtpa = Column(Float)
    start_year = Column(Integer)
    startup = Column(DateTime)

# ------------------------------------------------------
# CONTRACTS
# ------------------------------------------------------
class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))
    seller = Column(String(100), index=True)
    buyer = Column(String(100), index=True)
    capacity = Column(Float)
    delivery_mode = Column(String(20))
    start = Column(DateTime)
    end = Column(DateTime)
    origin_zone = Column(String(100))
    destination_zone = Column(String(100))
    UniqueConstraint('seller', 'buyer', 'start', name='uix_contract_unique')

# ------------------------------------------------------
# DIVERSIONS
# ------------------------------------------------------
class Diversion(Base):
    __tablename__ = "diversions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vessel = Column(String(100))
    diversion_date = Column(DateTime)
    origin_country = Column(String(100))
    diverted_from = Column(String(100))
    new_destination = Column(String(100))
    vessel_state = Column(String(50))
    charterer = Column(String(100))

# ------------------------------------------------------
# FLOWS
# ------------------------------------------------------
class Flow(Base):
    __tablename__ = "flows"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, index=True)
    country = Column(String(100), index=True)
    import_volume_twh = Column(Float)
    export_volume_twh = Column(Float)

# ------------------------------------------------------
# OUTAGES
# ------------------------------------------------------
class Outage(Base):
    __tablename__ = "outages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    outage_type = Column(String(50))
    installation_name = Column(String(100), ForeignKey("installations.installation"))
    installation_country = Column(String(100))
    start = Column(DateTime)
    end = Column(DateTime)
    comment = Column(String(200))
    installation = relationship("Installation", backref="outages")

# ------------------------------------------------------
# STORAGES (countries)
# ------------------------------------------------------
class StorageCountry(Base):
    __tablename__ = "storages_inv_countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, index=True)
    country = Column(String(100), index=True)
    inventory_twh = Column(Float)
    capacity_twh = Column(Float)
    fullness_pct = Column(Float)

# ------------------------------------------------------
# STORAGES (installations)
# ------------------------------------------------------
class StorageInstallation(Base):
    __tablename__ = "storages_inv_installations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, index=True)
    installation = Column(String(150), ForeignKey("installations.installation"))
    inventory_twh = Column(Float)
    capacity_twh = Column(Float)
    fullness_pct = Column(Float)
    installation_ref = relationship("Installation", backref="storage_levels")

# ------------------------------------------------------
# TRADES
# ------------------------------------------------------
class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_origin = Column(DateTime)
    date_destination = Column(DateTime)
    country_origin = Column(String(100))
    country_destination = Column(String(100))
    seller = Column(String(100))
    buyer = Column(String(100))
    vessel = Column(String(100))
    volume_twh = Column(Float)
