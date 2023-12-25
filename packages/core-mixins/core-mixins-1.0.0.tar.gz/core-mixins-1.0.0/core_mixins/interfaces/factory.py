# -*- coding: utf-8 -*-

from abc import ABC
from typing import Type, Dict, Self


class IFactory(ABC):
    """ Base interface for classes that acts like factories """

    _impls: Dict[str, Type[Self]] = {}

    def __init_subclass__(cls):
        cls._impls[cls.register_name()] = cls

    @classmethod
    def register_name(cls):
        """ It returns the name to use when the class is registered """
        return cls.__name__

    @classmethod
    def get_implementation(cls, registered_name: str) -> Type[Self]:
        """ It returns the implementation class by the registered name """
        return cls._impls.get(registered_name, None)
