from .iot import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets

# from modules.bluetooth import MyScanner
import asyncio


class Controller:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.selected_device = None
        self.available_devices = []

    def setSignals(self):
        self.ui.boton_configuracion_3.clicked.connect(self.scan_devices)
        self.ui.selec_10.currentIndexChanged.connect(self.leerModoOperacion)
        self.ui.selec_esp.currentIndexChanged.connect(self.set_device)
        self.ui.boton_detener.clicked.connect(self.criticalError)
        self.ui.boton_configuracion.clicked.connect(self.set_config)
        self.ui.boton_inicio.clicked.connect(self.start_connection)

    def scan_devices(self):
        # my_scanner = MyScanner()
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(my_scanner.run())
        # self.available_devices = my_scanner.get_devices()
        # print(f"Dispositivos encontrados: {self.available_devices}")
        # devices_names = [device.name for device, _ in self.available_devices]
        # self.ui.selec_esp.addItems(self.avaliable_devices)
        pass

    def set_device(self, index):
        # TODO: SET DEVICE
        if 0 <= index < len(self.available_devices):
            self.selected_device = self.available_devices[index]
            print(f"Se ha seleccionado el dispositivo: {self.selected_device}")
        else:
            self.throw_error_message(
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

    def leerModoOperacion(self):
        index = self.ui.selec_10.currentIndex()
        texto = self.ui.selec_10.itemText(index)
        print(texto)
        return texto

    def start_connection(self):
        # TODO: Connect selected_device with raspberry and send configuration
        ...

    def throw_error_message(self, message=""):
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

    def stop(self):
        print("Mori")
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
