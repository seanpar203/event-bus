""" Tests event being emitted and proper functions being called. """

from event_bus.bus import EventBus

# Constants
bus = EventBus()
TEST_VAR = 'Init'
EVENT_NAME = 'emit_test'


@bus.on(event=EVENT_NAME)
def subscription():
    global TEST_VAR
    TEST_VAR = 'Finished'


def test_event_emit():
    """ Tests that a function subscribed to an event executes on emit. """

    # Before Emit
    assert TEST_VAR == 'Init'

    bus.emit(EVENT_NAME)

    # After Emit
    assert TEST_VAR == 'Finished'
