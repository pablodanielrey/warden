import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from warden.model.entities.Warden import *

def crear_tablas():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['WARDEN_DB_USER'],
        os.environ['WARDEN_DB_PASSWORD'],
        os.environ['WARDEN_DB_HOST'],
        os.environ.get('WARDEN_DB_PORT',5432),
        os.environ['WARDEN_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)