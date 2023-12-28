"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from .common import NUMERIC
from .common import PARSABLE
from .times import Times



class Timer:
    """
    Track timers on unique key and determine when to proceed.

    .. testsetup::
       >>> from time import sleep

    Example
    -------
    >>> timer = Timer()
    >>> timer.create('test', 1)
    >>> timer.ready('test')
    False
    >>> sleep(1)
    >>> timer.ready('test')
    True

    :param mapping: Seconds that are used for each of timers.
    """

    __timer: dict[str, float]
    __cache: dict[str, Times]


    def __init__(
        self,
        mapping: Optional[dict[str, NUMERIC]] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        mapping = mapping or {}

        self.__timer = {
            k: float(v)
            for k, v in mapping.items()}

        self.__cache = {
            x: Times()
            for x in self.__timer}


    @property
    def mapping(
        self,
    ) -> dict[str, float]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return dict(self.__timer)


    def ready(
        self,
        unique: str,
        update: bool = True,
    ) -> bool:
        """
        Determine whether or not the appropriate time has passed.

        :param unique: Unique identifier for the timer in mapping.
        :param update: Determines whether or not time is updated.
        """

        timer = self.__timer
        cache = self.__cache

        if unique not in cache:
            raise ValueError('unique')

        _cache = cache[unique]
        _timer = timer[unique]

        ready = _cache.elapsed >= _timer

        if ready and update:
            self.update(unique)

        return ready


    def update(
        self,
        unique: str,
        started: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the existing timer from mapping within the cache.

        :param unique: Unique identifier for the timer in mapping.
        :param started: Override the start time for timer value.
        """

        cache = self.__cache

        if unique not in cache:
            raise ValueError('unique')

        cache[unique] = Times(started)


    def create(
        self,
        unique: str,
        minimum: int | float,
        started: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the existing timer from mapping within the cache.

        :param unique: Unique identifier for the timer in mapping.
        :param started: Determines when the time starts for timer.
        :param minimum: Determines minimum seconds that must pass.
        """

        timer = self.__timer
        cache = self.__cache

        if unique in cache:
            raise ValueError('unique')

        timer[unique] = float(minimum)

        cache[unique] = Times(started)
