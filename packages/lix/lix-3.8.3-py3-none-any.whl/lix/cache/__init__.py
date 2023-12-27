import sys
from functools import wraps
from collections import OrderedDict

class cache(object):
    '''
    Decorator to cache the return value of a function.

    Example:
        @cache
        def fib(n):
            if n < 2:
                return n
            return fib(n-1) + fib(n-2)
    '''
    def __init__(self, function):
        self.function = function
        self.cache = OrderedDict()
        self.shape = (0,)
        self.size = 0
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0

    def to(self, cache):
        self.cache = OrderedDict(cache)
        self.shape = (len(cache),)
        self.size = len(cache)
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0
        return self

    def index(self, index):
        if index >= 0 and index < len(self.cache):
            key = list(self.cache.keys())[index]
            value = self.cache[key]
            return key, value
        else:
            raise IndexError("cache.error\n\t> index out of range.")

    def keys(self):
        return tuple(self.cache.keys())

    def values(self):
        return tuple(self.cache.values())

    def items(self):
        return tuple(self.cache.items())

    def clear(self):
        self.cache.clear()
        self.shape = (self.size,)
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0
        return self

    def __call__(self, *args, **kwargs):
        key = (args, tuple(kwargs.items()))
        self.calls += 1
        try:
            if key in self.cache:
                self.hits += 1
                self.hit_rate = self.hits / self.calls
                return self.cache[key]
            else:
                self.misses += 1
                self.miss_rate = self.misses / self.calls
                result = self.function(*args, **kwargs)
                self.cache[key] = result
                self.call_rate = self.calls / (self.calls + self.misses)
                return result
        except Exception as e:
            excep_name:    str = e.__class__.__name__
            try:
                excep_line:    str = self.function.__code__.co_firstlineno
            except:
                excep_line:    str = 'unknown'
            exit(Exception(f"\n\nlimit.error(line={excep_line})\n\t> {excep_name}({e})\n\n"))

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __delitem__(self, key):
        del self.cache[key]

    def __len__(self):
        return self.size

    def __iter__ (self):
        return iter(self.cache)

    def __contains__(self, key):
        return key in self.cache

    def __repr__(self):
        return f"cache({self.function.__name__}, {self.shape}, {self.size})"

    def __str__(self):
        return f"cache({self.function.__name__}, {self.shape}, {self.size})"

class limit(object):
    '''
    Decorator to cache the return value of a function with a size limit.

    Example:
        @limit(5) # size=5
        def fib(n):
            if n < 2:
                return n
            return fib(n-1) + fib(n-2)
    '''
    def __init__(self, size):
        self.size = size
        self.shape = (size,)
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0
        self.root = self

    def to(self, cache):
        self.cache = OrderedDict(cache)
        self.shape = (len(cache),)
        self.size = len(cache)
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0
        return self

    def index(self, index):
        if index >= 0 and index < len(self.cache):
            key = list(self.cache.keys())[index]
            value = self.cache[key]
            return key, value
        else:
            raise IndexError("limit.error\n\t> index out of range.")

    def keys(self):
        return tuple(self.cache.keys())

    def values(self):
        return tuple(self.cache.values())

    def items(self):
        return tuple(self.cache.items())

    def clear(self):
        self.cache = OrderedDict()
        self.shape = (self.size,)
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.hit_rate = 0.0
        self.miss_rate = 0.0
        self.call_rate = 0.0
        return self

    def __call__(self, function):
        try:
            cache = OrderedDict()

            @wraps(function)
            def wrapper(*args, **kwargs):
                try:
                    key = (args, tuple(kwargs.items()))

                    if key in wrapper.cache:
                        wrapper.hits += 1
                        result = wrapper.cache[key]
                    else:
                        wrapper.misses += 1
                        result = function(*args, **kwargs)
                        wrapper.cache[key] = result
                        if len(wrapper.cache) > self.size:
                            wrapper.cache.popitem(last=False)

                    wrapper.calls += 1
                    wrapper.hit_rate = wrapper.hits / wrapper.calls
                    wrapper.miss_rate = wrapper.misses / wrapper.calls
                    wrapper.call_rate = wrapper.calls / (wrapper.hits + wrapper.misses)

                    return result
                except Exception as e:
                    excep_name:    str = e.__class__.__name__
                    try:
                        excep_line:    str = function.__code__.co_firstlineno
                    except:
                        excep_line:    str = 'unknown'
                    exit(Exception(f"\n\nlimit.error(line={excep_line})\n\t> {excep_name}({e})\n\n"))

            wrapper.cache = cache
            wrapper.calls = 0
            wrapper.hits = 0
            wrapper.misses = 0
            wrapper.call_rate = 0.0
            wrapper.hit_rate = 0.0
            wrapper.miss_rate = 0.0

            wrapper.to = self.to
            wrapper.index = self.index
            wrapper.keys = self.keys
            wrapper.values = self.values
            wrapper.items = self.items
            wrapper.clear = self.clear

            return wrapper
        except Exception as e:
            excep_name:    str = e.__class__.__name__
            try:
                excep_line:    str = self.function.__code__.co_firstlineno
            except:
                excep_line:    str = 'unknown'
            exit(Exception(f"\n\nlimit.error(line={excep_line})\n\t> {excep_name}({e})\n\n"))

    def manage(self):
        if len(self.cache) > self.size:
            self.cache.popitem(last=False)

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value
        self.manage()

    def __delitem__(self, key):
        del self.cache[key]

    def __len__(self):
        return len(self.cache)

    def __iter__(self):
        return iter(self.cache)

    def __contains__(self, key):
        return key in self.cache

    def __repr__(self):
        return f"limit(size={self.size})"

    def __str__(self):
        return f"limit(size={self.size})"

class fast(object):
    def __init__(self, function):
        self.function = function
        self.cache = {}

    def __call__(self, *args, **kwargs):
        try:
            key = (args, tuple(kwargs.items()))
            if key in self.cache:
                return self.cache[key]
            else:
                result = self.function(*args, **kwargs)
                self.cache[key] = result
                return result
        except Exception as e:
            excep_name:    str = e.__class__.__name__
            try:
                excep_line:    str = self.function.__code__.co_firstlineno
            except:
                excep_line:    str = 'unknown'
            exit(Exception(f"\n\fast.error(line={excep_line})\n\t> {excep_name}({e})\n\n"))

    def __repr__(self):
        return f"fast({self.function.__name__})"

    def __str__(self):
        return f"fast({self.function.__name__})"