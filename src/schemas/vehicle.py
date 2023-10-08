import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from db.postgre import db_url

metadata: MetaData = sqlalchemy.MetaData()

vehicles: sqlalchemy.sql.schema.Table = sqlalchemy.Table(
    'vehicles',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('vin', sqlalchemy.String(length=100)),
    sqlalchemy.Column('year', sqlalchemy.Integer),
    sqlalchemy.Column('make', sqlalchemy.String(length=100)),
    sqlalchemy.Column('model', sqlalchemy.String(length=100)),
    sqlalchemy.Column('type', sqlalchemy.String(length=100)),
    sqlalchemy.Column('color', sqlalchemy.String(length=100)),
    sqlalchemy.Column('weight', sqlalchemy.Float),
)

engine: Engine = sqlalchemy.create_engine(db_url, pool_size=3, max_overflow=0, echo=True)
metadata.create_all(engine)
