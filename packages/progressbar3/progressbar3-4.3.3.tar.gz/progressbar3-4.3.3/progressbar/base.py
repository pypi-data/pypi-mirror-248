class FalseMeta(type):
    @classmethod
    def __bool__(cls):  # pragma: no cover
        return False

    @classmethod
    def __cmp__(cls, other):  # pragma: no cover
        return -1

    __nonzero__ = __bool__


class UnknownLength(metaclass=FalseMeta):
    pass


class Undefined(metaclass=FalseMeta):
    pass
