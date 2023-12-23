class BaseType:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return f"{self._value}"

    def __repr__(self):
        return f"{self._value}"


class String(BaseType):
    pass


class Operand(BaseType):
    pass


class Operator(BaseType):
    pass


class Other(BaseType):
    pass


class Block(BaseType):
    pass
