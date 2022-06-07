class Register16(list):
    """16 bit registers """

    def __init__(self, value):
        self.append(value)

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

        bit_str = bit_str[0:key] + str(value) + bit_str[key + 1:]
        bit_str = bit_str[::-1]
        new_register = int("0b" + bit_str, base=2)
        super(Register16, self).__setitem__(0, new_register)

    def __getitem__(self, item):
        bit_str = self.as_bit_str()[::-1]
        return bit_str[item]

    def __int__(self):
        return super().__getitem__(0)
