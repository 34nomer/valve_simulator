from abc import ABC, abstractmethod
from register16 import Register16
from os import system


class Device(object):
    def __init__(self):
        self.lst_registers = []
        self.dct_settings = {}
        self.output_param = {}
        self.input_param = {}

    @abstractmethod
    def show(self):
        """"""

    @abstractmethod
    def auto_act(self):
        """"""

    @abstractmethod
    def management(self):
        """"""


class ZDV(Device):
    def __init__(self):
        super().__init__()
        for i in range(126):
            self.lst_registers.append(Register16(0))

    def show(self):
        for i in range(5):
            print(f"{i}: {self.lst_registers[i]}")

    def auto_act(self):
        pass
        return 0

    def management(self):
        system('cls') # Очистка экрана
        self.show()
        while True:
            command = input("""Введите команду в формате 
            <номер регистра>[<номер бита>]=<значение> — для изменения бита
            <номер регистра>=<значение> — для изменения значения
            q-для выхода""")
            if "q" in command.lower():
                break







