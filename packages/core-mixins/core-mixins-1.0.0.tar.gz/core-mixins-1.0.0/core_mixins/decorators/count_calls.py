# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps
from typing import Callable


class CountCalls:
    """ Decorator as class """

    def __init__(self, fcn: Callable):
        update_wrapper(self, fcn)
        self.calls_number = 0
        self.fcn = fcn

    def __call__(self, *args, **kwargs):
        self.calls_number += 1
        return self.fcn(*args, **kwargs)


def count_calls(fcn: Callable):
    """ Decorator as function """

    @wraps(fcn)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.calls_number += 1
        return fcn(*args, **kwargs)

    wrapper_count_calls.calls_number = 0
    return wrapper_count_calls
