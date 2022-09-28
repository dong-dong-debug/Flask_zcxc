from sqlalchemy import MetaData
from app import db


def dbconnect():
    dbsession = db.session
    DBase = db.Model
    metadata = MetaData(bind=db.engine)
    return dbsession, metadata, DBase
