from collections import namedtuple

__all__ = ['frozenclass']

class _Frozen:
    def __eq__(self, other) -> bool:
        cls = type(self)
        if type(other) is not cls:
            return False
        return self._data == other._data
    def __hash__(self) -> int:
        return self._data.__hash__()
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    def _init(self, **kwargs):
        cls = type(self)
        self._data = cls._Data(**kwargs)

class FGet:
    def __init__(self, name):
        name = str(name)
        if name[0] == '_':
            raise ValueError(name)
        self.__name__ = name
    def __call__(self, obj):
        return getattr(obj._data, self.__name__)


def frozenclass(arg, field_names=[]):
    field_names = list(field_names)
    for field_name in field_names:
        if field_name.startswith('_'):
            raise ValueError
    if type(arg) is str:
        typename = arg
        baseclasses = tuple()
    else:
        typename = arg.__name__
        baseclasses = (arg,)
    _Data = namedtuple(
        typename='_Data',
        field_names=list(field_names),
    )
    members = dict(
        _Data=_Data,
        __eq__=_Frozen.__eq__,
        __hash__=_Frozen.__hash__,
        __ne__=_Frozen.__ne__,
        _init=_Frozen._init,
    )
    for field_name in field_names:
        f = FGet(field_name)
        p = property(f)
        members[field_name] = p
    ans = type(
        typename,
        baseclasses,
        members,
    )
    return ans
    