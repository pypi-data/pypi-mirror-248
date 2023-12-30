from .attribute import NAttribute
from .object import NObject


class NBase(NObject):
    _type = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._ = self._type(*args, **kwargs)
