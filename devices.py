from abc import abstractmethod
from register16 import Register16
from os import system
from input_check import choice_function_from_dict
from input_check import choice_object_from_list


class Device(object):
    def __init__(self, name="1"):
        self.lst_registers = []
        self.dct_settings = {}
        self.state = {"name": name}

        self.dict_functions = {"show": self.show,
                               "auto": self.auto_act,
                               "register": self.set_register,
                               }

    @abstractmethod
    def show(self):
        """Показывает себя в консоли"""

    @abstractmethod
    def auto_act(self):
        """"""
    def __str__(self):
        """Кратко о себе"""
        return f"Устройство {self.state['name']} из {len(self.lst_registers)} регистров"

    def management(self):
        choice_function_from_dict(self.dict_functions, "Выберите, что вы хотите сделать")

    def set_register(self):
        """Изменение значения регистра"""
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

    def set_bit(self, register):
        """Установить бит в регистре"""
        print("вызвана функция Установить бит")
        user_bit_offset = ""
        user_bit = ""
        while user_bit_offset != "q":
            print(register)
            for bit in range(16):
                print(f"   {register.info_bit(bit)}")
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


class ZDV(Device):
    def __init__(self, name=1):
        super().__init__(name)
        for i in range(126):
            self.lst_registers.append(Register16(0))

        self.lst_registers[0].change_info("Технологический регистр")
        self.lst_registers[0].change_bit_info(0, '0 бит  1 – Механизм в положении «Открыто»')
        self.lst_registers[0].change_bit_info(1, '1 бит  1 – Механизм в положении «Закрыто»')
        self.lst_registers[0].change_bit_info(2, '2 бит  1 – Сработала муфта')
        self.lst_registers[0].change_bit_info(3, '3 бит  Резерв')
        self.lst_registers[0].change_bit_info(4, '4 бит  Резерв')
        self.lst_registers[0].change_bit_info(5, '5 бит  Резерв')
        self.lst_registers[0].change_bit_info(6, '6 бит  Резерв')
        self.lst_registers[0].change_bit_info(7, '7 бит  1 – Включён режим «Дистанционное управление»')
        self.lst_registers[0].change_bit_info(8, '8 бит  1 – Выполняется операция «Открытие»')
        self.lst_registers[0].change_bit_info(9, '9 бит  1 – Выполняется операция «Закрытие»')
        self.lst_registers[0].change_bit_info(10, '10 бит  1 – Режим работы «Стоп»')
        self.lst_registers[0].change_bit_info(11, '11 бит  Резерв')
        self.lst_registers[0].change_bit_info(12, '12 бит  Резерв')
        self.lst_registers[0].change_bit_info(13, '13 бит  1 – Включён подогрев блока')
        self.lst_registers[0].change_bit_info(14, '14 бит  Резерв')
        self.lst_registers[0].change_bit_info(15, '15 бит  Резерв')

        self.lst_registers[1].change_info("Регистр дефектов")

        self.lst_registers[1].change_bit_info(0, '0 бит  1 – Срабатывание время-токовой защиты')
        self.lst_registers[1].change_bit_info(1, '1 бит  1 – Срабатывание защиты от короткого' +
                                                 ' замыкания в цепи фаз двигателя')
        self.lst_registers[1].change_bit_info(2, '2 бит  1 – Срабатывание защиты от перегрева электродвигателя')
        self.lst_registers[1].change_bit_info(3,
                                              '3 бит  1 – Срабатывание защиты от пониженного напряжения входной сети')
        self.lst_registers[1].change_bit_info(4, '4 бит  Резерв')
        self.lst_registers[1].change_bit_info(5, '5 бит  1 – Срабатывание защиты «Отсутствие движения»')
        self.lst_registers[1].change_bit_info(6,
                                              '6 бит  1 – Срабатывание защиты от повышенного напряжения входной сети')
        self.lst_registers[1].change_bit_info(7, '7 бит  1 – Срабатывание защиты по обрыву фаз входной питающей сети')
        self.lst_registers[1].change_bit_info(8, '8 бит  Резерв')
        self.lst_registers[1].change_bit_info(9, '9 бит  1 – Срабатывание защиты по перегреву блока свыше 110˚С')
        self.lst_registers[1].change_bit_info(10, '10 бит  Резерв')
        self.lst_registers[1].change_bit_info(11, '11 бит  Резерв')
        self.lst_registers[1].change_bit_info(12, '12 бит  1 – Срабатывание защиты по неверному чередованию фаз' +
                                                  ' сети на силовом входе блока')
        self.lst_registers[1].change_bit_info(13,
                                              '13 бит  1 – Срабатывание защиты по неверному чередованию фаз двигателя')
        self.lst_registers[1].change_bit_info(14, '14 бит  Резерв')
        self.lst_registers[1].change_bit_info(15, '15 бит  Резерв')

        self.lst_registers[2].change_info("Регистр текущего положения")
        self.lst_registers[3].change_info("Регистр команд")

        self.dict_functions = {"auto": self.auto_act,
                               "command": self.get_command,
                               "registers": self.set_register,
                               "show": self.show}
        self.dict_commands = {"open": self.open,
                              "close": self.close,
                              "in_between": self.set_in_between,
                              "set_opened": self.open,
                              "set_closed": self.close,
                              }
        self.possible_state = {}

        self.state["full_stroke_time"] = 60
        self.state["dead_time"] = 10

    def show(self):
        """Показывает себя в консоли"""
        print(self.state["name"])
        for i in range(5):
            print(f"{i}: {self.lst_registers[i]}    | {int(self.lst_registers[i])}  | {self.lst_registers[i].info()}")

    def only_show(self):
        system('cls')  # Очистка экрана
        print("Должен быть чистый экран")
        self.show()
        return

    def auto_act(self):
        """Автоматический режим"""
        print("вызвана функция Автоматическое обновление модели")
        pass

    def get_command(self):
        """Подача команды управления"""
        choice_function_from_dict(self.dict_commands, "Выберите команду которую хотите подать")

    def open(self):
        """Пустить на открытие"""
        print("вызвана функция открыть задвижку")
        self.lst_registers[0][0] = 0  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 1  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 550  # Текущее положение от 0 до 1000

    def close(self):
        """Пустить на закрытие"""
        print("вызвана функция закрыть задвижку")
        self.lst_registers[0][0] = 0  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 1  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 450  # Текущее положение от 0 до 1000

    def stop(self):
        """остановить """
        print("вызвана функция остановить задвижку")
        self.lst_registers[0][0] = 0  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 500  # Текущее положение от 0 до 1000

    def set_in_between(self):
        """Оставить в промежутке """
        print("вызвана функция установить промежуток")
        self.lst_registers[0][0] = 0  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 500  # Текущее положение от 0 до 1000

    def set_opened(self):
        """Оставить открытой"""
        print("вызвана функция установить задвижку в положение 'Открыто'")
        self.lst_registers[0][0] = 1  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 1000  # Текущее положение от 0 до 1000

    def set_closed(self):
        """Оставить закрытой"""
        print("вызвана функция установить задвижку в положение 'Закрыто'")
        self.lst_registers[0][0] = 0  # 1-Механизм в положении "открыто"
        self.lst_registers[0][1] = 0  # 1-Механизм в положении "закрыто"
        self.lst_registers[0][2] = 0  # 1-Сработала муфта
        self.lst_registers[0][8] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[0][9] = 0  # 1 - Выполняется операция закрытия
        self.lst_registers[1][0] = 0  # 1-Срабатывание времятоковой защиты
        self.lst_registers[2] = 0  # Текущее положение от 0 до 1000

    def __str__(self):
        """Кратко о себе"""
        return f"Задвижка — {self.state['name']} "


class SimpleDevice(Device):
    """"Простое устройство"""
    MAX_SIZE = 200

    def __init__(self, name="1", size=100):
        super().__init__(name)
        for i in range(size):
            self.lst_registers.append(Register16(0))
        self.dict_functions = {"auto": self.auto_act,
                               "registers": self.set_register,
                               "show": self.show,
                               }
        self.state["name"] = name
        self.state["size"] = size
        self.possible_state = {}

    def auto_act(self):
        """Ничего не делает"""
        print("Выбрана команда автоматический")

    def show(self):
        """Показывает себя в консоли"""
        print(self.state["name"])
        size = self.state["size"]
        for i in range(size):
            print(f"{i}: {self.lst_registers[i]}    | {int(self.lst_registers[i])}")
