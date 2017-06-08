""" Tests the string representation of an EventBus class. """

from event_bus import EventBus

# Constants
bus = EventBus()
EVENT_NAME = 'completed'


@bus.on(event=EVENT_NAME)
def on_complete():
    """ Subscribed event to run after event `completed` """
    print("Hello World!")


def test_event_bus_str_repr():
    """ Tests what the str and repr magic methods return. """

    bus_str = str(bus)
    bus_repr = repr(bus)

    assert bus_str == "EventBus"
    assert bus_repr == "<EventBus: 1 subscribed events>"
