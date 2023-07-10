from peewee import (
    Model,
    IntegerField,
    FloatField,
    CharField,
    DateTimeField,
    TextField,
    ForeignKeyField,
)
from .database import db


class BaseModel(Model):
    class Meta:
        database = db


class Configuracion(BaseModel):
    protocol = IntegerField()
    transport_layer = IntegerField()


class Datos(BaseModel):
    id_device = CharField()
    MAC = CharField()
    transport_layer = IntegerField()
    protocol = IntegerField()
    length = IntegerField()
    Val1 = FloatField()
    Batt_level = FloatField()
    Timestamp = DateTimeField()
    Temp = FloatField(null=True)
    Press = FloatField(null=True)
    Hum = FloatField(null=True)
    Co = FloatField(null=True)
    RMS = FloatField(null=True)
    Amp_x = FloatField(null=True)
    Frec_x = FloatField(null=True)
    Amp_y = FloatField(null=True)
    Frec_y = FloatField(null=True)
    Amp_z = FloatField(null=True)
    Frec_z = FloatField(null=True)
    Acc_x = TextField(null=True)
    Acc_y = TextField(null=True)
    Acc_z = TextField(null=True)


class Logs(BaseModel):
    datos = ForeignKeyField(Datos)
    id_device = CharField()
    transport_layer = IntegerField()
    protocol = IntegerField()
    Timestamp = DateTimeField()


class Loss(BaseModel):
    time_to_connect = FloatField()
    connection_attempts = IntegerField()


# This function will create the tables
def create_tables():
    db.create_tables([Configuracion, Datos, Logs, Loss])
