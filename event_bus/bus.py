""" A simple event bus """

from functools import wraps
from collections import defaultdict, Counter
from typing import Iterable, Callable, List, Dict, Any


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

        self._events = defaultdict(list)  # type: Dict[Any, List[Callable]]

    def __repr__(self) -> str:
        """ Returns EventBus string representation.

        :return: Instance with how many subscribed events.
        """
        return self.__str__()

    def __str__(self) -> str:
        """ Returns EventBus string representation.

        :return: Instance with how many subscribed events.
        """

        count = self._subscribed_event_count()

        return "<{}: {} subscribed events.>".format(self._cls_name(), count)

    # ------------------------------------------
    # Public Methods
    # ------------------------------------------

    def on(self, event: str) -> Callable:
        """ Decorator for subscribing a function to a specific event.

        :param event: Name of the event to subscribe to.
        :type event: str

        :return: The outer function.
        :rtype: Callable
        """

        def outer(func):
            if func.__name__ not in self.event_func_names(event):
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
            of post processing without the callable requiring information
            before doing so.
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

    def event_func_names(self, name: str) -> List[str]:
        """ Returns string name of each function subscribed to an event.

        :param name: Name of the event.
        :type name: str

        :return: Names of functions subscribed to a specific event.
        :rtype: list
        """
        return [func.__name__ for func in self._events[name]]

    # ------------------------------------------
    #   Private Methods
    # ------------------------------------------

    def _cls_name(self) -> str:
        """ Convenience method to reduce verbosity.

        :return: Name of class
        :rtype: str
        """
        return self.__class__.__name__

    def _subscribed_event_count(self) -> int:
        """ Returns the total amount of subscribed events.

        :return: Integer amount events.
        :rtype: int
        """
        event_counter = Counter()  # type: Dict[Any, int]

        for key, values in self._events.items():
            event_counter[key] = len(values)

        return sum(event_counter.values())
