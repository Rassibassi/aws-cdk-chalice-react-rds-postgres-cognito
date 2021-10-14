import datetime

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

from chalicelib.db import db
from chalicelib.settings import Settings


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class User(BaseModel):
    name = CharField()

    class Meta:
        db_table = "users"


class Todo(BaseModel):
    user = ForeignKeyField(User, backref="todos")
    description = TextField()
    datetime = DateTimeField(default=datetime.datetime.now)


db_models = [User, Todo]

# if Settings.CHALICE_STAGE == "production":
#     for klass in db_models:
#         if not db.table_exists(klass.__name__):
#             db.create_tables([klass])
