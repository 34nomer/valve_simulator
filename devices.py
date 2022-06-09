from abc import ABC, abstractmethod
from register16 import Register16
from os import system
from input_check import choice_function_from_dict
from input_check import choice_object_from_list


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

    def set_bit(self, register):
        """установить бит в регистре"""
        print("вызвана функция Установить бит")
        user_bit_offset = ""
        user_bit = ""
        while user_bit_offset != "q":
            print(register)
            user_bit_offset = input("Введите номер бита")
            if user_bit_offset.isdigit():
                int_user_input = int(user_bit_offset)
                if 0 <= int_user_input <= 15:
                    while user_bit != "q":
                        user_bit = input("Введите значение бита")
                        if user_bit.isdigit():
                            user_bit_int = int(user_bit)
                            if 0 <= user_bit_int <= 1:
                                register[int_user_input] = user_bit_int
                                break
        return register

    def set_register(self):
        """изменение значения регистра"""
        print("вызвана функция установить новое значение регистра")
        count_regs = len(self.lst_registers)
        for i in range(count_regs):
            print(f"{i}: {self.lst_registers[i]}")
        register_offset = choice_object_from_list(self.lst_registers)
        if register_offset is None:
            return False

        if self.change_register(register_offset):
            print("значение регистра изменено")

    def change_register(self, offset):
        """Изменение регистра"""
        user_str = ""

        while True:
            user_str = input("введите новое значение регистра /n <b> для изменения битов мент")
            if user_str.lower() == "q":
                return None
            if user_str.lower() == "b":
                register = self.set_bit(self.lst_registers[offset])
                if register is None:
                    continue
                self.lst_registers[offset] = register
            if not user_str.isdigit():
                continue
            user_int = int(user_str)
            if 0 <= user_int <= 65535:
                self.lst_registers[offset] = Register16(user_int)
                return True

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
zdv1.show()
zdv1.management()
