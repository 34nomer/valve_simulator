from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets as QtW
from my_pyqt_widgets import ZDVWidget, warning_message
from devices import ZDV
import sys


class GuiImitator(QtW.QMainWindow):
    """Графика для имитатора
    """

    def __init__(self):
        super().__init__()

        # Настройка рамки главного окна
        self.setWindowTitle("Имитатор устройств")
        self.resize(600, 600)
        self.setWindowIcon(QIcon('pics\\zdv_pic.jpg'))

        self.statusBar().showMessage('Ready')

        # меню
        exit_action = QtW.QAction(QIcon('pics\\exit.png'), 'Закрыть', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtW.qApp.quit)

        new_device = QtW.QAction(QIcon('pics\\add_1.bmp'), "Новое устройство", self)
        new_device.setShortcut('Ctrl+A')
        new_device.setStatusTip('Добавить устройство')
        new_device.triggered.connect(self.add_device)

        delete_device = QtW.QAction(QIcon('pics\\del.bmp'), "Удалить устройство", self)
        delete_device.setShortcut('Ctrl+X')
        delete_device.setStatusTip('Удалить устройство')
        delete_device.triggered.connect(self.remove_current_zdv)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addAction(exit_action)

        devices_menu = menubar.addMenu("Устройства")
        devices_menu.addAction(new_device)
        devices_menu.addAction(delete_device)

        # Тул бар
        self.toolbar = self.addToolBar('Выход')
        self.toolbar.addAction(exit_action)
        self.toolbar.addAction(new_device)
        self.toolbar.addAction(delete_device)
        network_settings = {"port": "com1",
                            "parity": "None",
                            "baud_rate": "9600"}

        # главный виджет главного окна с вертикальной разметкой
        self.central_widget = QtW.QWidget(self)
        self.vbox_central_widget = QtW.QVBoxLayout(self.central_widget)
        self.network_widget = NetworkGui(self, network_settings)
        self.vbox_central_widget.addWidget(self.network_widget)

        self.device_tab = DeviceTab(self.central_widget)
        self.vbox_central_widget.addWidget(self.device_tab)

        self.accessible_devices = ("ZDV", "simple_device")
        self.device_list = []
        self.device_tab.update_state(self.device_list)
        self.setCentralWidget(self.central_widget)

    def closeEvent(self, e):
        """Уточнить при выходе
        """

        reply = QtW.QMessageBox.question(self, "Подтверждение выхода",
                                         "Хотите выйти ?", QtW.QMessageBox.Yes |
                                         QtW.QMessageBox.No, QtW.QMessageBox.No)
        if reply == QtW.QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()

    def add_device(self):
        dialog = DeviceAdditionDialog(self)
        dialog.show()

    def remove_current_zdv(self):
        curent_device_index = self.device_tab.currentIndex()
        released_adress = self.device_list[curent_device_index].adress
        self.network_widget.free_adresses_lst.append(released_adress)
        self.device_list.pop(curent_device_index)
        self.device_tab.update_state(self.device_list)


class DeviceAdditionDialog(QtW.QDialog):
    def __init__(self, parent):
        super(DeviceAdditionDialog, self).__init__(parent)
        self.setWindowTitle("Добавление устройства")
        self.layout = QtW.QVBoxLayout(self)
        self.devices = parent.accessible_devices
        self.parent = parent
        self.free_addresses = self.parent.network_widget.free_adresses_lst

        self.button_box = QtW.QDialogButtonBox(self)
        self.button_box.setStandardButtons(QtW.QDialogButtonBox.Cancel | QtW.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.the_editing_finished)
        self.button_box.rejected.connect(self.reject)

        self.choice_device_lbl = QtW.QLabel("Выберите устройство из списка", self)
        self.choice_device_combox = QtW.QComboBox(self)
        for devices in self.devices:
            self.choice_device_combox.addItem(str(devices))
        self.select_layout = QtW.QFormLayout()
        self.select_layout.setWidget(0, QtW.QFormLayout.LabelRole, self.choice_device_lbl)
        self.select_layout.setWidget(0, QtW.QFormLayout.FieldRole, self.choice_device_combox)

        self.choice_adress_lbl = QtW.QLabel("Введите адрес", self)
        self.choice_adress_le = QtW.QLineEdit(self)
        self.choice_adress_le.setToolTip("Введите число от 1 до 247")
        self.select_layout.setWidget(1, QtW.QFormLayout.LabelRole, self.choice_adress_lbl)
        self.select_layout.setWidget(1, QtW.QFormLayout.FieldRole, self.choice_adress_le)

        self.name_lbl = QtW.QLabel("Введите название устройства", self)
        self.name_le = QtW.QLineEdit(self)
        self.name_le.setToolTip("Не должно быть пустым")
        self.select_layout.setWidget(2, QtW.QFormLayout.LabelRole, self.name_lbl)
        self.select_layout.setWidget(2, QtW.QFormLayout.FieldRole, self.name_le)

        self.layout.addLayout(self.select_layout)
        self.layout.addWidget(self.button_box)

    def the_editing_finished(self):
        if self.choice_device_combox.currentText() == "simple_device":
            warning_message(title="simple_devise", text="Устройство simple device пока что не реализовано")
            return
        inputted_address = self.choice_adress_le.text()
        if not inputted_address.isdigit():
            warning_message(title="Некорректное значение", text="Введите число")
            self.choice_adress_le.setText("")
            return
        int_inputted_address = int(inputted_address)
        if not (1 <= int_inputted_address <= 247):
            warning_message(title="Некорректное значение", text="Введите число от 1 до 247")
            self.choice_adress_le.setText("")
            return
        if not (int_inputted_address in self.free_addresses):
            warning_message(title="Некорректное значение", text="Возможно адрес занят")
            self.choice_adress_le.setText("")
            return
        if self.name_le.text() == "":
            warning_message(title="Некорректное значение", text="Введите имя устройства")
            return

        self.create_device(device=self.choice_device_combox.currentText(),
                           adress=int_inputted_address,
                           name=self.name_le.text())

        self.reject()

    def create_device(self, device, adress, name):
        if device == "simple_device":
            return

        if self.choice_device_combox.currentText() == "ZDV":
            zdv = ZDV(name)
            zdv.adress = adress
            self.parent.device_list.append(zdv)
            self.parent.device_tab.update_state(self.parent.device_list)
            self.free_addresses.remove(adress)


class NetworkGui(QtW.QFrame):
    """Виджет состояния сети
    """

    def __init__(self, parent_widget, network_settings: dict):
        super(NetworkGui, self).__init__(parent_widget)
        self.setFrameShadow(QtW.QFrame.Sunken)
        self.setFrameShape(QtW.QFrame.Box)
        self.settings = network_settings
        self.lbl_list = []
        self.horizontalLayout = QtW.QHBoxLayout(self)

        port = QtW.QLabel()
        port.setText(f"Порт{self.settings['port']}" if 'port' in self.settings else "no port")
        port.sizeHint()
        self.lbl_list.append(port)
        baud_rate = QtW.QLabel()
        baud_rate.setText(f"Скорость{self.settings['baud_rate']}" if 'baud_rate' in self.settings else "no baud rate")
        baud_rate.sizeHint()
        self.lbl_list.append(baud_rate)
        parity = QtW.QLabel()
        parity.setText(f"Четность{self.settings['parity']}" if 'parity' in self.settings else "no parity check")
        parity.sizeHint()
        self.lbl_list.append(parity)

        for label in self.lbl_list:
            self.horizontalLayout.addWidget(label)
        self.free_adresses_lst = [x for x in range(1, 247)]





class DeviceTab(QtW.QTabWidget):
    """Таблица с устройствами"""

    def __init__(self, parent):
        super(DeviceTab, self).__init__(parent)
        self.device_lst = []

    def update_state(self, device_list):
        while len(self.device_lst) > 0:
            self.device_lst.pop(0)
            self.removeTab(0)
            print(self.device_lst)
        print("Вышли из цикла")
        print(self.device_lst)
        for device in device_list:
            self.add_device(device)

    def add_device(self, device):
        device = ZDVWidget(device)
        self.addTab(device, str(device))
        self.device_lst.append(device)

    def delete_device(self, device):
        if device not in self.device_lst:
            print("попытка удалить устройство которого нет")
            return
        deleted_tab = self.device_lst.index(str(device))
        self.removeTab(deleted_tab)
        self.device_lst.pop(deleted_tab)
        print(str(deleted_tab) + " is deleted tab")


if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)
    model = GuiImitator()
    model.show()
    sys.exit(app.exec_())
