from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QAction, qApp
from PyQt5 import QtWidgets as QtW
from devices import ZDV
from register16 import Register16
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
        exit_action = QtW.QAction(QIcon('pics\\exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtW.qApp.quit)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(exit_action)

        # Тул бар
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exit_action)
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

        self.device_list = [ZDV("входная агрегатная"), ZDV("выкидная"), ZDV("восьмая"),
                            ZDV("третья"), ZDV("четвертая"), ZDV("пятая"),
                            ZDV("шестая"), ZDV("седьмая"),
                            ]
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
        parity.setText(f"Четность{self.settings['parity']}" if 'parity' in self.settings else "no pariry check")
        parity.sizeHint()
        self.lbl_list.append(parity)

        for label in self.lbl_list:
            self.horizontalLayout.addWidget(label)


class DeviceTab(QtW.QTabWidget):
    """Таблица с устройствами"""
    def __init__(self, parent):
        super(DeviceTab, self).__init__(parent)
        self.device_lst = []

    def update_state(self, deviсe_lst):
        while len(self.device_lst) > 0:
            self.device_lst.pop(0)
            self.removeTab(0)
            print(self.device_lst)
        print("Вышли из цикла")
        print(self.device_lst)
        for device in deviсe_lst:
            self.add_device(device)# TODO подставить сюда наши виджеты

    def add_device(self, device):  # TODO подставить сюда наши виджеты
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


class ZDVWidget(QtW.QWidget):
    """Виджет отображение задвижки
    """
    def __init__(self, zdv):
        super(ZDVWidget, self).__init__()
        self.zdv = zdv
        self.vbox = QtW.QVBoxLayout(self)
        self.vbox.setObjectName("vbox")
        self.state_lbl = QtW.QLabel(str(self.zdv) + " Состояние ")

        self.automaticaly_rb = QtW.QRadioButton(self)
        self.automaticaly_rb.setText("Автоматический режим")
        self.manual_rb = QtW.QRadioButton(self)
        self.manual_rb.setText("Ручной режим")
        self.mode_select_btn = QtW.QPushButton("режим", self)
        self.mode_layout = QtW.QHBoxLayout()
        self.mode_layout.addWidget(self.automaticaly_rb)
        self.mode_layout.addWidget(self.manual_rb)
        self.mode_layout.addWidget(self.mode_select_btn)
        self.register_widgets = []
        for i in range(4):
            self.register_widgets.append(RegisterWidget(register=self.zdv.lst_registers[i],
                                                        parent=self))

        self.progressBar = QtW.QProgressBar(self)
        self.progressBar.setValue(24)
        self.full_stroke_time_le = QtW.QLineEdit(self)
        self.dead_time_le = QtW.QLineEdit(self)
        self.full_stroke_time_lbl = QtW.QLabel("Время полного хода")
        self.dead_time_lbl = QtW.QLabel("Время схода с концевиков")
        self.time_form_layout = QtW.QFormLayout()
        self.time_form_layout.setWidget(0, QtW.QFormLayout.LabelRole, self.full_stroke_time_lbl)
        self.time_form_layout.setWidget(0, QtW.QFormLayout.FieldRole, self.full_stroke_time_le)
        self.time_form_layout.setWidget(1, QtW.QFormLayout.LabelRole, self.dead_time_lbl)
        self.time_form_layout.setWidget(1, QtW.QFormLayout.FieldRole, self.dead_time_le)
        self.vbox.addWidget(self.state_lbl)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.mode_layout)
        self.vbox.addLayout(self.time_form_layout)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.progressBar)
        for widget in self.register_widgets:
            self.vbox.addWidget(widget)

    def __str__(self):
        return str(self.zdv)


class RegisterWidget(QtW.QWidget):
    def __init__(self, register, parent):
        super(RegisterWidget, self).__init__(parent)
        self.register = register
        self.info_register_lbl = QtW.QLabel(register.info())
        self.value_register_lbl = QtW.QLabel(f"{register}  |  {int(register)}")
        self.layout = QtW.QHBoxLayout(self)
        self.layout.addWidget(self.info_register_lbl)
        self.layout.addWidget(self.value_register_lbl)

    def mouseDoubleClickEvent(self, event):
        dialog = ChangeRegisterDialog(self)
        dialog.show()


class ChangeRegisterDialog(QtW.QDialog):
    def __init__(self, parent):
        super(ChangeRegisterDialog, self).__init__(parent)
        self.register = parent.register
        self.input_line = QtW.QLineEdit()
        self.setWindowTitle("Обновите значение регистра")
        q_btn = QtW.QDialogButtonBox.Ok | QtW.QDialogButtonBox.Cancel
        self.button_box = QtW.QDialogButtonBox(q_btn)
        self.layout = QtW.QVBoxLayout(self)
        message = QtW.QLabel(self.register.info())
        self.bit_checkboxes = []
        for bit in range(16):
            bit_checkbox = QtW.QCheckBox(self.register.info_bit(bit))
            self.bit_checkboxes.append(bit_checkbox)

        self.layout.addWidget(message)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.button_box)
        for bit_checkbox in self.bit_checkboxes:
            self.layout.addWidget(bit_checkbox)

    def editingFinished(self, event):
        print(event)

        user_value = self.input_line.text()

        if not user_value.isdigit():
            # self.input_line.setText("")
            return
        int_user_value = int(user_value)
        if 0 <= int_user_value < 2**16:
            self.register[0] = 1
        return


if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)
    model = GuiImitator()
    model.show()
    sys.exit(app.exec_())