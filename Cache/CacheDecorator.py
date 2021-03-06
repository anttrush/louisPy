from io import StringIO
import pandas as pd
import json
import warnings
from Cache.SimpleContainer import SimpleContainer


class Cache:

    def __init__(self, redis_instance=None):
        if not redis_instance:
            self.cache_container = SimpleContainer()
            warnings.warn("No Redis instance Specified, ttl feature disabled, cache will stay in memory forever.")
        else:
            if type(redis_instance.echo("hello")) == str:
                self.cache_container = redis_instance
            else:
                raise AttributeError(
                    "Redis instance's decode_responses must be set True. Use StrictRedis(..., decode_responses=True)")

    def ttl(self, ttl=None):
        def enable(func):
            def func_wrapper(*args, **kwargs):
                target_key = ":".join(["CACHE", func.__name__, *[str(i) for i in args], str(kwargs)])
                target_key = hash(target_key)
                a = self.cache_container.get(target_key)
                if a:
                    return a
                else:
                    result = func(*args, **kwargs)
                    self.cache_container.set(target_key, result, ttl)
                    return result

            return func_wrapper

        return enable

    def ser_df(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs).to_csv(index=False)
        func_wrapper.__name__ = name
        return func_wrapper

    def de_ser_df(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return pd.read_csv(StringIO(func(*args, **kwargs)))
        func_wrapper.__name__ = name
        return func_wrapper

    def df(self, ttl=None):
        def deco(func):
            for dec in [self.ser_df, self.ttl(ttl), self.de_ser_df]:
                func = dec(func)
            return func

        return deco

    def ser_number(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return str(func(*args, **kwargs))
        func_wrapper.__name__ = name
        return func_wrapper

    def de_ser_int(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return int(func(*args, **kwargs))
        func_wrapper.__name__ = name
        return func_wrapper

    def de_ser_float(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return float(func(*args, **kwargs))
        func_wrapper.__name__ = name
        return func_wrapper

    def int(self, ttl=None):
        def deco(func):
            for dec in [self.ser_number, self.ttl(ttl), self.de_ser_int]:
                func = dec(func)
            return func

        return deco

    def float(self, ttl=None):
        def deco(func):
            for dec in [self.ser_number, self.ttl(ttl), self.de_ser_float]:
                func = dec(func)
            return func

        return deco

    def ser_dict(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return json.dumps(func(*args, **kwargs))
        func_wrapper.__name__ = name
        return func_wrapper

    def de_ser_dict(self, func):
        name = func.__name__
        def func_wrapper(*args, **kwargs):
            return json.loads(func(*args, **kwargs))
        func_wrapper.__name__ = name
        return func_wrapper

    def dict(self, ttl=None):
        def deco(func):
            for dec in [self.ser_dict, self.ttl(ttl), self.de_ser_dict]:
                func = dec(func)
            return func

        return deco


if __name__ == '__main__':
    pass
