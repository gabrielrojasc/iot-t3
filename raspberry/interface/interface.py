from .iot import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets

from modules.bluetooth import MyScanner
from modules import wifi_server
import asyncio

ALL_STATUS = [0, 20, 21, 22, 23, 30, 31]
ALL_PROTOCOLS = [1, 2, 3, 4, 5]
BLE_STATUS = [0, 30, 31]
WIFI_STATUS = [20, 21, 22, 23]


class Controller:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.device = None
        self.advertisement_data = None
        self.available_devices = []
        self.status = 0
        self.protocol = 1
        self.config = None
        # TODO: Obtener de la base de datos:
        # {status_select_index: (status, [protocols])}
        self.status_protocol = {
            0: (0, [1]),  # config_by_bluetooth
            1: (20, [1]),  # config_by_tcp
            2: (21, [1, 2, 3, 4, 5]),  # tcp_continuous
            3: (22, [1, 2, 3, 4, 5]),  # tcp_discontinuous
            4: (23, [1, 2, 3, 4, 5]),  # udp
            5: (30, [1, 2, 3, 4]),  # ble_continuous
            6: (31, [1, 2, 3, 4]),  # ble_discontinuous
        }

    def setSignals(self):
        # Scan Devices
        self.ui.boton_configuracion_3.clicked.connect(self.scan_devices)
        # Select Device
        self.ui.selec_esp.currentIndexChanged.connect(self.set_device)
        # Select Status
        self.ui.selec_10.currentIndexChanged.connect(self.set_operation_mode)
        # Select Protocol
        self.ui.selec_11.currentIndexChanged.connect(self.set_operation_mode)
        # Set Configuration
        self.ui.boton_configuracion.clicked.connect(self.set_config)
        # Start Connection
        self.ui.boton_inicio.clicked.connect(self.start_connection)
        # Stop Connection
        self.ui.boton_detener.clicked.connect(self.stop_connection)

    def scan_devices(self):
        print("Escaneando dispositivos disponibles...")
        # my_scanner = MyScanner()
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(my_scanner.run())
        # self.available_devices = my_scanner.get_devices()
        # print(f"Dispositivos encontrados: {self.available_devices}")
        # devices_names = [device.name for device, _ in self.available_devices]
        # self.ui.selec_esp.addItems(devices_names)
        pass

    def set_device(self, index):
        # TODO: SET DEVICE
        if 0 <= index < len(self.available_devices):
            self.device, self.advertisement_data = self.available_devices[index]
            print(f"Se ha seleccionado el dispositivo: {self.device}")
        else:
            self.show_error_message(
                f"El índice {index} seleccionado fuera del rango de opciones {self.available_devices}"
            )

    def read_config(self):
        conf = dict()
        conf["acc_samp"] = self.ui.text_acc_sampling.toPlainText()
        conf["acc_sen"] = self.ui.text_acc_sensibity.toPlainText()
        conf["gyro_sen"] = self.ui.text_gyro_sensibility.toPlainText()
        conf["bme688"] = self.ui.textEdit_18.toPlainText()
        conf["disc_time"] = self.ui.text_disc_time.toPlainText()
        conf["tcp_port"] = self.ui.text_tcp_port.toPlainText()
        conf["udp_port"] = self.ui.text_udp_port.toPlainText()
        conf["host_ip"] = self.ui.text_host_ip.toPlainText()
        conf["ssid"] = self.ui.text_ssid.toPlainText()
        conf["password"] = self.ui.text_pass.toPlainText()
        print(conf)
        return conf

    def set_config(self):
        # if self.selected_device:
        config = self.read_config()
        # TODO: Configurar device con self.config
        # TODO: Revisar si es válida

    def read_operation_mode(self):
        status_index = self.ui.selec_10.currentIndex()
        status_selected = self.ui.selec_10.itemText(status_index)
        protocol_index = self.ui.selec_11.currentIndex()
        protocol_selected = self.ui.selec_11.itemText(protocol_index)
        print(status_selected, protocol_selected)
        return (status_index, protocol_index)

    def set_operation_mode(self):
        status_index, protocol_index = self.read_operation_mode()
        status = protocol = -1
        if 0 <= status_index < len(self.status_protocol):
            status = self.status_protocol[status_index][0]
        else:
            return self.show_error_message(
                f"Error: Status de índice {status_index} no existe"
            )
        if 0 <= protocol_index < len(self.status_protocol[status_index][1]):
            protocol = self.status_protocol[status_index][1][protocol_index]
        else:
            return self.show_error_message(
                f"Error: Protocolo de índice {protocol_index} no es válido para {status=}"
            )
        self.status = status
        self.protocol = protocol

    def start_connection(self):
        # TODO: Connect selected_device with raspberry and send configuration
        if not self.is_device_ready_for_connection():
            return

        # BLE Connection
        if self.status in BLE_STATUS:
            print(f"Empezando conexión BLE con dispositivo: {self.device.name}")
            print(f"Starting with {self.protocol=}, {self.status=}")
            print()
            # Nota: service_uuids puede venir vacia. Quizás debamos guardar manualmente el characteristics_uuid
            sm = StateMachine(
                self.status,
                str(self.protocol),
                self.device.address,
                self.advertisement_data.service_uuids[0],
            )
            sm.start()
        # TODO: WIFI Connection
        # WIFI Connection
        elif self.status in WIFI_STATUS:
            print(f"Empezando conexión Wifi con dispositivo: {self.device.name}")
            print(f"Configurado con {self.status} y {self.protocol=}")
            # MAIN WIFI
            wifi_server.run(
                self.config["host"],
                self.config["tcp_port"],
                self.config["udp_port"],
                self.status,
                self.protocol,
            )
            # TODO: Implementar que cuando el puerto esté ocupado aparezca un
            # mensaje de error informando. Así puedo intentar de nuevo desde la
            # interfaz hasta que funcione. Quizás hacer un try except o algo

    # Checks if device has been selected and has a valid configuration
    def is_device_ready_for_connection(self):
        if self.device == None:
            self.show_error_message(
                f"No se ha seleccionado un dispositivo a conectar: {self.device}"
            )
        # elif TODO: VALIDAR CONFIG
        elif self.protocol not in ALL_PROTOCOLS:
            self.show_error_message(f"Protocolo {self.protocol} no es válido")
        elif self.status not in ALL_STATUS:
            self.show_error_message(f"Status {self.status} no es válido")
        else:
            return True
        return False

    def show_error_message(self, message=""):
        popup = QtWidgets.QMessageBox(parent=self.parent)
        popup.setWindowTitle("Ha ocurrido un error inesperado")
        popup.setText(message)
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
        return

    def criticalError(self):
        popup = QtWidgets.QMessageBox(parent=self.parent)
        popup.setWindowTitle("ERROR MASIVO")
        popup.setText("QUE HAS APRETADO, NOS HAS CONDENADO A TODOS")
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
        return

    def stop_connection(self):
        # TODO: Detener conexión entre ESP y Raspberry
        # Sinceramente no se me ocurre de 1era como hacer esto
        print(f"Deteniendo conexión con dispositivo {self.device}...")
        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    cont = Controller(parent=Dialog)
    ui = cont.ui
    ui.setupUi(Dialog)
    Dialog.show()
    cont.setSignals()
    sys.exit(app.exec_())
