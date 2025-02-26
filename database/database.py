from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField
)

from config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True)
    username = CharField(unique=True)


def create_models() -> None:
    db.create_tables(BaseModel.__subclasses__())