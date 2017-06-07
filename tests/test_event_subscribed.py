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

    # Convenience variables
    func_name = subscription.__name__
    event_func_names = bus.event_func_names(EVENT_NAME)
    event_count = bus.subscribed_event_count()

    # Asserts
    assert func_name in event_func_names
    assert event_count == 1
