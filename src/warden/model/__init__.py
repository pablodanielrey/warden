import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@contextlib.contextmanager
def obtener_session(echo=False):
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['WARDEN_DB_USER'],
        os.environ['WARDEN_DB_PASSWORD'],
        os.environ['WARDEN_DB_HOST'],
        os.environ.get('WARDEN_DB_PORT',5432),
        os.environ['WARDEN_DB_NAME']
    ), echo=echo)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

def crear_tablas():
    from warden.model.WardenModel import *
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['WARDEN_DB_USER'],
        os.environ['WARDEN_DB_PASSWORD'],
        os.environ['WARDEN_DB_HOST'],
        os.environ.get('WARDEN_DB_PORT',5432),
        os.environ['WARDEN_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)