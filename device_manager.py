from devices import ZDV, SimpleDevice
from input_check import choice_function_from_dict, choice_object_from_list


class DeviceManager(object):
    def __init__(self):
        self.lst_devices = []
        self.state = {}
        self.possible_devise = {"zdv": self.create_zdv,
                                "simple": self.create_simple_device,
                                }
        self.possible_action = {"add": self.add_device,
                                "delete": self.delete_device,
                                "show": self.show_devices}

    def add_device(self):
        """Добавить устройство"""
        choice_function_from_dict(self.possible_devise, "Выберите, объект который вы хотите сделать")

    def create_zdv(self):
        """Создать задвижку"""
        name = input("введите имя задвижки, <q> для выхода ")
        if name.lower() == "q":
            return
        if name == "":
            ordinal_number = len(self.lst_devices) + 1
            name = f'Задвижка №{ordinal_number}'
        print(f"Создать задвижку с именем: {name}")
        self.lst_devices.append(ZDV(name))

    def create_simple_device(self):
        """Создать простое устройство"""
        name = input("введите имя устройства, <q> для выхода ")
        if name.lower() == "q":
            return
        if name == "":
            ordinal_number = len(self.lst_devices) + 1
            name = f'Устройство №{ordinal_number}'

        number_register = -1
        while not (0 < number_register <= SimpleDevice.MAX_SIZE):
            number_register = input(f"Введите количество регистров не больше {SimpleDevice.MAX_SIZE}")
            number_register = int(number_register) if number_register.isdigit() else -1

            # TODO Переделать

        assert 0 < int(number_register) <= SimpleDevice.MAX_SIZE
        print(f"Создать устройство с именем:{name}, размером {number_register}")
        self.lst_devices.append(SimpleDevice(name=name, size=int(number_register)))

    def delete_device(self):
        """Удалить устройство"""
        print("вызвана функция удалить устройство")
        index = choice_object_from_list(self.lst_devices, "введите номер удаляемого устройства")
        if index is not None:
            print("Должно удалиться из списка устройств")
            self.lst_devices.pop(index)

    def show_devices(self):
        """Показать все устройства"""
        print("Выбрана функция показать все устройства")
        for device in self.lst_devices:
            print("*" * 79)
            device.show()

    def get_command(self):
        """Подать каманду"""
        choice_function_from_dict(self.possible_action, "Выберите, команду которую вы хотите подать ")


