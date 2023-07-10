import json
import datetime
from .models import Datos, Logs, Loss, Configuracion


def get_configs():
    configs = Configuracion.select().tuples()
    return list(configs)


def data_save(header, data):
    now = datetime.datetime.now()

    # Get the Timestamp of the last row to calculate the Timedelay
    Datos.select().order_by(Datos.id.desc()).get()

    # Create a new Datos object
    new_data = Datos.create(
        id_device=header["id_device"],
        MAC=header["MAC"],
        transport_layer=header["transport_layer"],
        protocol=header["protocol"],
        length=header["length"],
        Val1=data["Val: 1"],
        Batt_level=data["Batt_level"],
        Timestamp=data["Timestamp"],
        Temp=data.get("Temp"),
        Press=data.get("Press"),
        Hum=data.get("Hum"),
        Co=data.get("Co"),
        RMS=data.get("RMS"),
        Amp_x=data.get("Amp_x"),
        Frec_x=data.get("Frec_x"),
        Amp_y=data.get("Amp_y"),
        Frec_y=data.get("Frec_y"),
        Amp_z=data.get("Amp_z"),
        Frec_z=data.get("Frec_z"),
        Acc_x=json.dumps(data.get("Acc_x")),
        Acc_y=json.dumps(data.get("Acc_y")),
        Acc_z=json.dumps(data.get("Acc_z")),
    )

    # Update Datos for specific protocols
    if header["protocol"] in [1, 2, 3, 4]:
        Datos.update(
            Temp=data.get("Temp"),
            Press=data.get("Press"),
            Hum=data.get("Hum"),
            Co=data.get("Co"),
        ).where(
            Datos.id == new_data.id,
        ).execute()

    if header["protocol"] in [2, 3]:
        Datos.update(
            RMS=data.get("RMS"),
        ).where(
            Datos.id == new_data.id,
        ).execute()

    if header["protocol"] == 3:
        Datos.update(
            Amp_x=data.get("Amp_x"),
            Frec_x=data.get("Frec_x"),
            Amp_y=data.get("Amp_y"),
            Frec_y=data.get("Frec_y"),
            Amp_z=data.get("Amp_z"),
            Frec_z=data.get("Frec_z"),
        ).where(Datos.id == new_data.id).execute()

    if header["protocol"] == 4:
        Datos.update(
            Acc_x=data.get("Acc_x"),
            Acc_y=data.get("Acc_y"),
            Acc_z=data.get("Acc_z"),
        ).where(
            Datos.id == new_data.id,
        ).execute()

    # Create a new Logs object
    Logs.create(
        datos=new_data,
        id_device=header["id_device"],
        transport_layer=header["transport_layer"],
        protocol=header["protocol"],
        Timestamp=now,
    )


def save_loss(time_to_connect, connection_attempts):
    Loss.create(
        time_to_connect=time_to_connect,
        connection_attempts=connection_attempts,
    )
