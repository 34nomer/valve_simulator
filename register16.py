class Register16(list):
    """16 bit registers """
    REGISTER_STATE = ()

    def __init__(self, value):
        super(Register16, self).__init__()
        self.append(value)
        self._info = "Простой регистр"
        self._info_bit = [f"{i} бит" for i in range(16)]

    def as_bit_str(self):
        """returns its own value as a string of bits

        """

        bit_str = bin(super().__getitem__(0))[2:]
        return "0" * (16 - len(bit_str)) + bit_str

    def __str__(self):
        bit_str = self.as_bit_str()
        return f'{bit_str[0:4]}_{bit_str[4:8]}_{bit_str[8:12]}_{bit_str[12:16]}'

    def __setitem__(self, key, value):
        bit_str = self.as_bit_str()[::-1]
        if isinstance(value, bool):
            value = "1" if value else "0"
        if isinstance(value, int):
            value = "1" if value == 1 else "0"

        assert isinstance(value, str)
        assert value == "0" or value == "1"

        bit_str = bit_str[0:key] + value + bit_str[key + 1:]
        bit_str = bit_str[::-1]
        new_register = int("0b" + bit_str, base=2)
        super(Register16, self).__setitem__(0, new_register)

    def __getitem__(self, item):
        bit_str = self.as_bit_str()[::-1]
        return bit_str[item] == "1"

    def __int__(self):
        return super().__getitem__(0)

    def info(self):
        """return information about the register"""
        return self._info

    def info_bit(self, bit: int):
        """return information about the bit in the register"""
        assert isinstance(bit, int)
        assert 0 <= bit <= 15
        return self._info_bit[bit]

    def change_info(self, new_info):
        assert isinstance(new_info, str)
        self._info = new_info
        return 0

    def change_bit_info(self, bit: int, new_bit_info: str):
        assert isinstance(bit, int)
        assert 0 <= bit <= 15
        assert isinstance(new_bit_info, str)
        self._info_bit[bit] = new_bit_info

    def new_value(self, value: int):
        assert isinstance(value, int),  "Ожидается Значение INT"
        if 0 <= value < 2**16:
            register = Register16(value)
            for i in range(16):
                self[i] = register[i]
            return 0
        return 1
