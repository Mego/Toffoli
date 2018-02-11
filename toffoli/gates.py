import operator
from functools import reduce


class Gate:
    gate_registry = {}

    def __init__(self, identifier, *inputs):
        self.identifier = identifier
        self.inputs = inputs
        self.input_values = None
        self.value = None  # :(
        Gate.gate_registry[identifier] = self

    def compute_value(self):
        raise NotImplementedError

    def fetch_inputs(self):
        raise NotImplementedError


class ConstantGate(Gate):
    def __init__(self, identifier, value, *inputs):
        super(Gate, self).__init__(identifier, *inputs)
        self.value = value

    def compute_value(self):
        pass

    def fetch_inputs(self):
        pass


class ToffoliGate(Gate):
    def __init__(self, identifier, *inputs):
        super().__init__(identifier, *inputs)

    def compute_value(self):
        output_values = self.input_values[:-1]
        output_values.append(reduce(operator.and_, output_values) ^ self.input_values[-1])
        self.value = output_values

    def fetch_inputs(self):
        self.input_values = [g.value for g in self.inputs]


ZERO = ConstantGate("0", 0)
ONE = ConstantGate("1", 1)


def get_gate_by_id(identifier):
    return Gate.gate_registry[identifier]


def do_tick():
    for gate in Gate.gate_registry.values():
        gate.fetch_inputs()
    for gate in Gate.gate_registry.values():
        gate.compute_value()

