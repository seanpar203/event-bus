""" Tests event being emitted and proper functions being called. """

from event_bus.bus import EventBus

# Constants
bus = EventBus()
GLOBAL_VAR = 'Init'
EVENT_NAME = 'completed'


@bus.on(event=EVENT_NAME)
def subscription():
    """ Subscribed event to run after event `completed` """
    global GLOBAL_VAR
    GLOBAL_VAR = 'Finished'


def test_event_emit():
    """ Tests that a function subscribed to an event executes on emit. """

    # Before Emit
    assert GLOBAL_VAR == 'Init'

    bus.emit(EVENT_NAME)

    # After Emit
    assert GLOBAL_VAR == 'Finished'
