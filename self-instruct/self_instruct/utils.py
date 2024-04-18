import warnings
import functools

try:
    from deprecated import deprecated
except ImportError:
    print("[INFO] Using custom deprecated decorator.")
    def deprecated(func):
        """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used."""
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn("Call to deprecated function {}.".format(func.__name__),
                        category=DeprecationWarning,
                        stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        return new_func

class AttrDict:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(self, key, AttrDict(**value))
            else:
                setattr(self, key, value)
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, value):
        setattr(self, key, value)
        
def dump_dataclass(object):
    if isinstance(object, AttrDict):
        return dump_dataclass(object.__dict__)
    if isinstance(object, int) \
    or isinstance(object, str) \
    or isinstance(object, float) \
    or isinstance(object, bool) \
    or object is None:
        return object
    if isinstance(object, list):
        return list(map(dump_dataclass, object))
    if isinstance(object, dict):
        return dict(map(lambda e: (e[0], dump_dataclass(e[1])), object.items()))
    return dict(map(lambda e: (e[0], dump_dataclass(e[1])), object.__dict__.items()))