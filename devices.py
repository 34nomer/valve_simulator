from abc import ABC, abstractmethod
from register16 import Register16
from os import system


class Device(object):
    def __init__(self):
        self.lst_registers = []
        self.dct_settings = {}
        self.state = {}


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
                               "command": self.get_command,
                               "registers": self.set_register,
                               }
        self.dict_commands = {"open": self.open,
                              "close": self.close,
                              "in_between": self.set_in_between,
                              "set_opened": self.open,
                              "set_closed": self.close,
                              }
        self.state = {}
        self.possible_state = {}

    def show(self):
        for i in range(5):
            print(f"{i}: {self.lst_registers[i]}")

    def only_show(self):
        system('cls')  # Очистка экрана
        print("Должен быть чистый экран")
        self.show()
        return

    def auto_act(self):
        print("вызвана функция Автоматическое обновление модели")
        pass

    def get_command(self):
        print("вызвана функция Установить новый параметр")
        user_input = ""
        while user_input.lower() != "q":
            self.only_show()
            print("q - для выхода ")
            for command in self.dict_commands:
                print("выберите функцию")
                print(f"{command} ")
            user_input = input()
            for command in self.dict_commands:
                if user_input.lower() == command:
                    self.dict_commands[command]()
            if command.lower() == "q":
                continue
            else:
                print("Неизвестная команда")

    def set_bit(self):
        print("вызвана функция Установить бит")
        pass

    def set_register(self):
        print("вызвана функция установить новое значение регистра")

    def open(self):
        print("вызвана функция открыть задвижку")

    def close(self):
        print("вызвана функция закрыть задвижку")

    def stop(self):
        print("вызвана функция остановить задвижку")

    def set_in_between(self):
        print("вызвана функция установить промежуток")

    def set_opened(self):
        print("вызвана функция установить задвижку в положение 'Открыто'")

    def set_closed(self):
        print("вызвана функция установить задвижку в положение 'Закрыто'")

    def management(self):

        user_input = ""
        while user_input.lower() != "q":
            self.only_show()
            print("q - для выхода ")
            print("выберите функцию")
            for function in self.dict_functions:
                print(f"{function}")
            user_input = input()
            for function in self.dict_functions:
                if user_input.lower() == function:
                    self.dict_functions[function]()
            if user_input.lower() == "q":
                continue
            else:
                print("Неизвестная команда")





zdv1 = ZDV()

zdv1.management()


