""" Tests removing subscribed events. """

from event_bus import EventBus

bus = EventBus()

# Constants(Well kinda, we manipulate them in subscribed events)
EVENT_NAME = 'event'


@bus.on(event=EVENT_NAME)
def event_one():
    pass


def test_suscribed_event_was_removed():
    """ Checks to make sure that the removal of subscribed event works. """
    before_count = bus.subscribed_event_count()

    bus.remove_subscriber(event=EVENT_NAME, func_name=event_one.__name__)

    after_count = bus.subscribed_event_count()

    assert before_count == 1
    assert after_count == 0
