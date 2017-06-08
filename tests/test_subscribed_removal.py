""" Tests removing subscribed events. """

from event_bus import EventBus
from event_bus.exceptions import EventDoesntExist

bus = EventBus()

# Constants(Well kinda, we manipulate them in subscribed events)
EVENT_NAME = 'event'


@bus.on(event=EVENT_NAME)
def event_one():
    """ Mock event. """
    pass


def test_suscribed_event_was_removed():
    """ Checks to make sure that the removal of subscribed event works. """
    before_count = bus.event_count

    bus.remove_event(event=EVENT_NAME, func_name=event_one.__name__)

    after_count = bus.event_count

    assert before_count == 1
    assert after_count == 0


def test_removing_event_that_doest_exist():
    """ Checks to make sure that the removal of subscribed event works. """
    before_count = bus.event_count

    try:
        bus.remove_event(event=EVENT_NAME, func_name='hello')
    except EventDoesntExist:
        assert before_count == bus.event_count
