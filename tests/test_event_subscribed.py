""" Tests that a function is actually subscribed to an event. """

from event_bus.bus import EventBus

# Constants
bus = EventBus()
EVENT_NAME = 'hello_world'


@bus.on(event=EVENT_NAME)
def subscription():
    """ Subscribed event to run after event `hello_world` """
    print("Hello World!")


def test_event_subscription():
    """ Tests that a function is subscribed to an event. """

    # Asserts
    assert bus.event_count == 1
