from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

database = SqliteDatabase('taco.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(UserMixin, BaseModel):
    email = CharField(unique=True)
    password = CharField(max_length=20)

    @classmethod
    def create_user(cls, email, password):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Taco(BaseModel):
    user = ForeignKeyField(User)
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = CharField()

    @classmethod
    def create_taco(cls, user, protein, shell, cheese, extras):
        cls.create(
            user=user,
            protein=protein,
            shell=shell,
            cheese=cheese,
            extras=extras
        )


def initialize():
    database.connect()
    database.create_tables([User,Taco],safe=True)
    database.close()