""" Exceptions for EventBus. """


class EventDoesntExist(Exception):
    """ Raised when trying remove an event that doesn't exist. """
    pass
