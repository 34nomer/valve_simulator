from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets as QtW


class ZDVWidget(QtW.QWidget):
    """Виджет отображение задвижки
    """

    def __init__(self, zdv):
        super(ZDVWidget, self).__init__()
        self.zdv = zdv
        self.vbox = QtW.QVBoxLayout(self)
        self.vbox.setObjectName("vbox")
        self.state_lbl = QtW.QLabel(str(self.zdv) + " Состояние " + self.zdv.state["main_state"])

        self.automaticaly_rb = QtW.QRadioButton(self)
        self.automaticaly_rb.setText("Автоматический режим")
        self.automaticaly_rb.clicked.connect(self.set_auto_mod)

        self.manual_rb = QtW.QRadioButton(self)
        self.manual_rb.setText("Ручной режим")
        self.manual_rb.clicked.connect(self.set_manual_mod)
        self.manual_rb.setChecked(not self.zdv.state["auto_mod"])

        self.mode_select_btn = QtW.QPushButton("Перейти в ручной режим" if self.zdv.state["auto_mod"]
                                               else "Перейти в автоматический режим", self)
        self.mode_select_btn.clicked.connect(lambda: self.set_auto_mod() if not self.zdv.state["auto_mod"]
                                             else self.set_manual_mod())
        self.mode_layout = QtW.QHBoxLayout()
        self.mode_layout.addWidget(self.automaticaly_rb)
        self.mode_layout.addWidget(self.manual_rb)
        self.mode_layout.addWidget(self.mode_select_btn)

        self.control_btns_lst = []
        self.open_btn = QtW.QPushButton("Открыть", self)
        self.open_btn.clicked.connect(self.zdv.open)
        self.control_btns_lst.append(self.open_btn)

        self.stop_btn = QtW.QPushButton("Стоп", self)
        self.stop_btn.clicked.connect(self.zdv.stop)
        self.control_btns_lst.append(self.stop_btn)

        self.close_btn = QtW.QPushButton("Закрыть", self)
        self.close_btn.clicked.connect(self.zdv.close)
        self.control_btns_lst.append(self.close_btn)

        for btn in self.control_btns_lst:
            btn.setEnabled(self.zdv.state["auto_mod"])

        self.control_btn_layout = QtW.QHBoxLayout()
        self.control_btn_layout.addWidget(self.open_btn)
        self.control_btn_layout.addWidget(self.stop_btn)
        self.control_btn_layout.addWidget(self.close_btn)

        self.auto_run_timer = QTimer(self)
        self.auto_run_timer.timeout.connect(self.update)
        self.zdv.state["update_time"] = 500

        self.register_widgets = []
        for i in range(4):
            self.register_widgets.append(RegisterWidget(register=self.zdv.lst_registers[i],
                                                        parent=self))

        self.progressBar = QtW.QProgressBar(self)
        self.progressBar.setValue(int(self.zdv.lst_registers[2])//10)
        self.progressBar.setToolTip("Процент открытия")

        self.full_stroke_time_le = QtW.QLineEdit(self)
        self.full_stroke_time_le.setText(f"{self.zdv.state['full_stroke_time']}")
        self.full_stroke_time_le.setToolTip("число от 5 до 600")
        self.full_stroke_time_le.editingFinished.connect(self.change_full_stroke_time)
        self.full_stroke_time_lbl = QtW.QLabel("Время полного хода, c")

        self.dead_time_le = QtW.QLineEdit(self)
        self.dead_time_le.setText(f"{self.zdv.state['dead_time']}")
        self.dead_time_lbl = QtW.QLabel("Время схода с концевиков, c")
        self.dead_time_le.setToolTip("число до четверти времени хода")
        self.dead_time_le.editingFinished.connect(self.change_dead_time)

        self.time_form_layout = QtW.QFormLayout()
        self.time_form_layout.setWidget(0, QtW.QFormLayout.LabelRole, self.full_stroke_time_lbl)
        self.time_form_layout.setWidget(0, QtW.QFormLayout.FieldRole, self.full_stroke_time_le)
        self.time_form_layout.setWidget(1, QtW.QFormLayout.LabelRole, self.dead_time_lbl)
        self.time_form_layout.setWidget(1, QtW.QFormLayout.FieldRole, self.dead_time_le)
        self.vbox.addWidget(self.state_lbl)
        self.vbox.addLayout(self.mode_layout)

        self.vbox.addWidget(self.progressBar)
        self.vbox.addLayout(self.control_btn_layout)
        for widget in self.register_widgets:
            self.vbox.addWidget(widget)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.time_form_layout)

    def __str__(self):
        return f"({self.zdv.adress}) {self.zdv}"

    def change_full_stroke_time(self):
        new_full_stroke_time = self.full_stroke_time_le.text()
        if new_full_stroke_time.isdigit():
            if 5 <= int(new_full_stroke_time) <= 600:
                self.zdv.state["full_stroke_time"] = int(new_full_stroke_time)
                self.full_stroke_time_le.setText(f'{self.zdv.state["full_stroke_time"]}')
                print("Значение полный ход задвижки изменено")
            else:
                print("введите корректное значение")
                self.full_stroke_time_le.setText(f'введите корректное значение')
        else:
            self.full_stroke_time_le.setText(f'введите число')
        return

    def change_dead_time(self):
        new_dead_time = self.dead_time_le.text()
        if new_dead_time.isdigit():
            if 0 <= int(new_dead_time) <= self.zdv.state["full_stroke_time"] // 4:
                self.zdv.state["dead_time"] = int(new_dead_time)
                self.dead_time_le.setText(f'{self.zdv.state["dead_time"]}')
                print("Значение времени схода с концевика изменено")
            else:
                print("введите корректное значение")
                self.dead_time_le.setText(f'введите корректное значение')
        else:
            self.dead_time_le.setText(f'введите число')
        return

    def set_auto_mod(self,):

        self.automaticaly_rb.setChecked(True)
        self.mode_select_btn.setText("Перейти в ручной режим")
        self.zdv.state["auto_mod"] = True
        self.auto_run_timer.start(self.zdv.state["update_time"])
        for btn in self.control_btns_lst:
            btn.setEnabled(self.zdv.state["auto_mod"])

    def set_manual_mod(self,):

        self.manual_rb.setChecked(True)
        self.mode_select_btn.setText("Перейти в автоматический режим")
        self.zdv.state["auto_mod"] = False
        self.auto_run_timer.stop()
        for btn in self.control_btns_lst:
            btn.setEnabled(self.zdv.state["auto_mod"])

    def update(self):
        super(ZDVWidget, self).update()
        self.zdv.auto_act()
        self.state_lbl.setText(str(self.zdv) + " Состояние " + self.zdv.state["main_state"])
        self.progressBar.setValue(int(self.zdv.lst_registers[2])//10)
        for register_wdg in self.register_widgets:
            register_wdg.update()


class RegisterWidget(QtW.QWidget):
    def __init__(self, register, parent):
        super(RegisterWidget, self).__init__(parent)
        self.register = register
        self.info_register_lbl = QtW.QLabel(register.info())
        self.value_register_lbl = QtW.QLabel(f"{register}  |  {int(register)}")
        self.layout = QtW.QHBoxLayout(self)
        self.layout.addWidget(self.info_register_lbl)
        self.layout.addWidget(self.value_register_lbl)
        self.setToolTip("Двойной щелчок для редактирования")
        self.setStatusTip(register.info())

    def update(self):
        super(RegisterWidget, self).update()
        self.value_register_lbl.setText(f"{self.register}  |  {int(self.register)}")

    def mouseDoubleClickEvent(self, event):
        dialog = ChangeRegisterDialog(self)
        dialog.show()


class ChangeRegisterDialog(QtW.QDialog):
    def __init__(self, parent):
        super(ChangeRegisterDialog, self).__init__(parent)
        self.parent = parent
        self.register = parent.register
        self.input_line = QtW.QLineEdit()
        self.input_line.setText(f"{int(self.register)}")
        self.setWindowTitle("Обновите значение регистра")
        q_btn = QtW.QDialogButtonBox.Ok | QtW.QDialogButtonBox.Cancel
        self.button_box = QtW.QDialogButtonBox(q_btn)
        self.button_box.button(QtW.QDialogButtonBox.Ok).setText("Применить")
        self.button_box.accepted.connect(self.the_editing_finished)
        self.button_box.rejected.connect(self.reject)

        self.layout = QtW.QVBoxLayout(self)
        message = QtW.QLabel(self.register.info())
        self.bit_checkboxes = []
        for bit in range(16):
            bit_checkbox = QtW.QCheckBox(self.register.info_bit(bit))
            print(self.register[bit])
            bit_checkbox.setChecked((self.register[bit]))
            bit_checkbox.clicked.connect(self.change_bit)
            self.bit_checkboxes.append(bit_checkbox)

        self.layout.addWidget(message)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.button_box)
        for bit_checkbox in self.bit_checkboxes:
            self.layout.addWidget(bit_checkbox)

    def change_bit(self):
        print("Установить бит")
        for i, checkbox in enumerate(self.bit_checkboxes):
            if checkbox.isChecked():
                self.register[i] = 1
            else:
                self.register[i] = 0
        self.input_line.setText(f"{int(self.register)}")
        self.parent.update()
        return

    def the_editing_finished(self):
        print("жмакнута применить ")
        user_value = self.input_line.text()
        if not user_value.isdigit():
            self.input_line.setText(f"введите число от {0} до {2 ** 16 - 1}")
            return
        int_user_value = int(user_value)
        if 0 <= int_user_value < 2 ** 16:
            self.register.new_value(int_user_value)
            print(self.register)
            self.parent.update()
            for bit, bit_checkbox in enumerate(self.bit_checkboxes):
                bit_checkbox.setChecked((self.register[bit]))
        else:
            self.input_line.setText(f"введите число от {0} до {2 ** 16 - 1}")
        return


def warning_message(title, text):
    assert isinstance(title, str)
    assert isinstance(text, str)
    msg = QtW.QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QtW.QMessageBox.Warning)
    msg.exec_()
    return
