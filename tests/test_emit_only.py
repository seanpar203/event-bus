""" Tests emitting specific events. """

from event_bus import EventBus

bus = EventBus()

# Constants(Well kinda, we manipulate them in subscribed events)
EVENT_NAME = 'event'

GLOBAL_VAR_1 = 'var_1'
GLOBAL_VAR_2 = 'var_2'


# Lets create 3 events subscribed to the same event.
# The last event is the control and shouldn't run with emit_only

@bus.on(event=EVENT_NAME)
def event_one():
    global GLOBAL_VAR_1
    GLOBAL_VAR_1 = 'change_1'


@bus.on(event=EVENT_NAME)
def event_two():
    global GLOBAL_VAR_2
    GLOBAL_VAR_2 = 'change_2'


@bus.on(event=EVENT_NAME)
def event_control():
    global GLOBAL_VAR_2
    GLOBAL_VAR_2 = 'change_3'


def test_emitting_specific_function():
    """ Tests specific event emitting. """

    # Syntax emit only.
    bus.emit_only(EVENT_NAME, func_names=['event_one', 'event_two'])

    assert GLOBAL_VAR_1 == 'change_1'
    assert GLOBAL_VAR_2 == 'change_2'
