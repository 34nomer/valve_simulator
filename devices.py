from abc import ABC, abstractmethod
from register16 import Register16
from os import system
from input_check import choice_function_from_dict

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
        """автоматический режим"""
        print("вызвана функция Автоматическое обновление модели")
        pass

    def get_command(self):
        """подача команды управления"""
        choice_function_from_dict(self.dict_commands, "Выберите команду которую хотите подать")

    def set_bit(self):
        """установить бит в регистре"""
        print("вызвана функция Установить бит")
        pass

    def set_register(self):
        """изменение значения регистра"""
        print("вызвана функция установить новое значение регистра")

    def open(self):
        """пустить на открытие"""
        print("вызвана функция открыть задвижку")

    def close(self):
        """пустить на закрытие"""
        print("вызвана функция закрыть задвижку")

    def stop(self):
        """остановить """
        print("вызвана функция остановить задвижку")

    def set_in_between(self):
        """оставить в промежутке """
        print("вызвана функция установить промежуток")

    def set_opened(self):
        """оставить открытой"""
        print("вызвана функция установить задвижку в положение 'Открыто'")

    def set_closed(self):
        """оставить закрытой"""
        print("вызвана функция установить задвижку в положение 'Закрыто'")

    def management(self):
        choice_function_from_dict(self.dict_functions, "Выберите, что вы хотите сделать")






zdv1 = ZDV()

zdv1.management()


