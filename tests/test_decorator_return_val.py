""" Test the emitted functions return value."""

from event_bus import EventBus

bus = EventBus()
EVENT_NAME = 'completed'


@bus.on(event=EVENT_NAME)
def on_completed():
    """ Subscribed event to run after event `completed` """
    return "It works!"


def test_decorator_return_val():
    """ Tests tha the decorator returns value. """
    returned = on_completed()

    assert returned == "It works!"
