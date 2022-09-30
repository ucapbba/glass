# author: Nicolas Tessore <n.tessore@ucl.ac.uk>
# license: MIT
'''module for generator definition'''

from functools import wraps, partial


class Generator:
    '''wrapper for generators with named receives and yields'''

    __slots__ = 'generator', 'receives', 'yields', 'initial'

    def __new__(cls, generator=None, *args, **kwargs):
        '''only create a generator wrapper if not already wrapped'''
        if isinstance(generator, cls):
            obj = generator
        else:
            obj = object.__new__(cls)
            object.__setattr__(obj, 'receives', None)
            object.__setattr__(obj, 'yields', None)
            object.__setattr__(obj, 'initial', None)
        return obj

    def __init__(self, generator=None, receives=None, yields=None, initial=None):
        '''wrap a generator'''
        if generator is not self:
            self.generator = generator
        if receives is not None:
            self.receives = receives
        if yields is not None:
            self.yields = yields
        if initial is not None:
            self.initial = initial

    def __iter__(self):
        '''call iter() on wrapped generator'''
        return iter(self.generator)

    def __next__(self):
        '''call next() on wrapped generator'''
        return next(self.generator)

    def __getattr__(self, name):
        '''get an attribute of the wrapped generator'''
        if name in self.__slots__:
            obj = self
        else:
            obj = self.generator
        return object.__getattribute__(obj, name)

    def __setattr__(self, name, value):
        '''set an attribute of the wrapped generator'''
        if name in self.__slots__:
            obj = self
        else:
            obj = self.generator
        object.__setattr__(obj, name, value)


def wrap_generator(f, *, self=False, receives=None, yields=None, initial=None):
    '''wrap a function that returns a generator'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        if self:
            g = Generator(None, receives, yields, initial)
            g.generator = f(g, *args, **kwargs)
        else:
            generator = f(*args, **kwargs)
            g = Generator(generator, receives, yields, initial)
        return g
    return wrapper


def self(f):
    '''decorator to make a self-referential generator'''
    return wrap_generator(f, self=True)


def _stripargs(first=None, *other):
    '''strip args tuple'''
    return [first, *other] if other else first


def receives(*args):
    '''decorator to label inputs of generator functions'''
    return partial(wrap_generator, receives=_stripargs(*args))


def yields(*args):
    '''decorator to label outputs of generator functions'''
    return partial(wrap_generator, yields=_stripargs(*args))


def initial(*args):
    '''decorator to label initial output of generator functions'''
    return partial(wrap_generator, initial=_stripargs(*args))
