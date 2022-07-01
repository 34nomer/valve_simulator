PORT_POSSIBLE_STATES = (None, "com1", "com2", "com3", "com4", "com5")
STOP_BIT_POSSIBLE_STATES = (None, "1", "1.5", "2")
PARITY_POSSIBLE_STATES = (None, "even", "none", "odd")
BAUD_RATE = (None, "19200", "9600")


class Parameter(object):
    def __init__(self, name: "str", value=None, ):
        self.name = name
        self.value = value
        self.possible_states = None
        self.numer = 0

    def __str__(self):
        return f"{self.value}"

    def info(self):
        return f"{self.name} - {self.value}"

    def set_possible_states(self, new_states):
        """

        """
        self.possible_states = list(new_states)

    def add_possible_states(self, new_state):
        self.possible_states.append(new_state)

    def new_value(self, new_value):
        assert not bool(self.possible_states) or (bool(self.possible_states) and new_value in self.possible_states)
        self.value = new_value

    def empty(self):
        return self.value is None
