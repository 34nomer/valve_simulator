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
        self.dict_functions = {"auto": self.auto_act,
                           "state": self.set_state,
                           "registers": self.set_register,
                               }

    def show(self):
        for i in range(5):
            print(f"{i}: {self.lst_registers[i]}")

    def only_show(self):
        system('cls')  # Очистка экрана
        self.show()
        return

    def auto_act(self):
        print("вызвана функция Автоматическое обновление модели")
        pass

    def set_state(self):
        print("вызвана функция Установить новый параметр")
        pass

    def set_bit(self):
        print("вызвана функция Установить бит")
        pass

    def set_register(self):
        print("вызвана функция установить новое значение регистра")

    def management(self):

        command = ""
        while command.lower() != "q":
            self.only_show()
            for function in self.dict_functions:
                print("q - для выхода ")
                print("выберите функцию")
                print(f"{function}: enter the command ")
            command = input()
            for function in self.dict_functions:
                if command.lower() == function:
                    self.dict_functions[function]()
            if command.lower() == "q":
                continue
            else:
                print("Неизвестная команда")








