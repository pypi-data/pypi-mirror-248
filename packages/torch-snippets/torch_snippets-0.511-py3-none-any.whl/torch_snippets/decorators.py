# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/decorators.ipynb.

# %% auto 0
__all__ = ['timeit', 'io', 'check_kwargs_not_none']

# %% ../nbs/decorators.ipynb 2
from functools import wraps
from .inspector import inspect
from .logger import Info
import time

# %% ../nbs/decorators.ipynb 3
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        output = func(*args, **kwargs)
        end = time.time()
        Info(f"{func.__name__} took {end-start:.2f} seconds to execute")
        return output

    return wrapper


def io(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) != 0:
            inspect(args, names=["inputs:args"])
        if kwargs != {}:
            inspect(kwargs, names=["inputs:kwargs"])
        output = func(*args, **kwargs)
        inspect(output, names=["outputs"])
        return output

    return wrapper


def check_kwargs_not_none(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                raise ValueError(f"Input argument '{key}' cannot be None")
        return func(*args, **kwargs)

    return wrapper
