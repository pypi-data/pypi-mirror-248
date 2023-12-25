# -*- coding: utf-8 -*-

from functools import wraps
from time import perf_counter
from typing import Callable


def timer(fcn: Callable = None, precision: int = 4):
    def decorator_timer(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time, res = perf_counter(), func(*args, **kwargs)
            return res, f"{(perf_counter() - start_time):.{precision}f}"

        return wrapper_timer

    if not fcn:
        return decorator_timer

    return decorator_timer(fcn)
