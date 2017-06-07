""" Tests that a subscribed event is run after. """

from event_bus import EventBus

bus = EventBus()
GLOBAL_VAR = 'Init'
EVENT_NAME = 'completed'


@bus.on(event=EVENT_NAME)
def on_complete():
    """ Subscribed function to EVENT_NAME """

    global GLOBAL_VAR
    GLOBAL_VAR = 'Finished'


@bus.emit_after(event=EVENT_NAME)
def code():
    """ A function that emits an event after completion. """

    print("Application code.")


def test_event_after():
    """ Tests that the event runs after. """

    code()
    assert GLOBAL_VAR == 'Finished'
