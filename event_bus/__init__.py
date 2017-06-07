# -*- coding: utf-8 -*-
""" A simple event bus """

from functools import wraps
from collections import defaultdict
from typing import Iterable, Callable, List


class EventBus:
    """ A simple event bus class. """

    # ------------------------------------------
    #   Dunder Attrs
    # ------------------------------------------

    __slots__ = ('_events',)

    # ------------------------------------------
    #   Dunder Methods
    # ------------------------------------------

    def __init__(self) -> None:
        """ Creates new EventBus object. """

        self._events = defaultdict(list)

    def __str__(self) -> str:
        """ Returns string representation. """
        return "<{}>".format(self.__class__.__name__)

    # ------------------------------------------
    #   Public Methods
    # ------------------------------------------

    def on(self, event: str) -> Callable:
        """ Creates a function(s) to be called when an event is emitted.

        :param event: Name of the event to subscribe to.
        :type event: str
        """

        def outer(func):
            if id(func) not in self._event_funcs_ids(event):
                self._events[event].append(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def emit(self, event: str, *args, **kwargs) -> None:
        """ Emit an event and run the subscribed functions.

        :param event: Name of the event.
        :type event: str 
        """
        for func in self.event_funcs(event):
            func(*args, *kwargs)

    def emit_after(self, event: str) -> Callable:
        """ Decorator that emits events after the function is completed. 

        :param event: The first parameter
        :type event: str

        :return: Callable
        
         :Note:
            This plainly just calls functions without passing params into the
            subscribed callables. This is great if you want to do some kind
            of post processing without requiring information before doing so. 
        """

        def outer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, *kwargs)
                self.emit(event)

            return wrapper

        return outer

    def event_funcs(self, name: str) -> Iterable[Callable]:
        """ Returns an Iterable of the functions subscribed to a event.

        :param name: Name of the event.
        :type name: str

        :return: A iterable to do things with.
        :rtype: Iterable
        """
        for func in self._events[name]:
            yield func

    # ------------------------------------------
    #   Private Methods
    # ------------------------------------------

    def _event_funcs_ids(self, name: str) -> List[int]:
        """ Returns unique ids of each function subscribed to an event.

        :param name: Name of the event.
        :type name: str
        :return: 
        """
        return [id(func) for func in self._events[name]]
