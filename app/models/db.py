import databases
import ormar
import sqlalchemy
from fastapi import FastAPI

DATABASE_URL = "sqlite:///data/db.sqlite"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


def init_db(app: FastAPI):
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    app.state.database = database
