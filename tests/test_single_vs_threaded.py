from time import time
from threading import Thread

# Libs
from event_bus import EventBus

bus = EventBus()

SINGLE_THREADED = 'single'
MULTI_THREADED = 'multi'


def create_single_threaded_events():
    for i in range(20):
        @bus.on(event=SINGLE_THREADED)
        def fib(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fib(n - 1) + fib(n - 2)


def create_multi_threaded_events():
    for i in range(20):
        @bus.on(event=MULTI_THREADED)
        def fib(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fib(n - 1) + fib(n - 2)


def test_single_vs_threaded():
    """ On a very small scale this tests that threaded outperforms single. """
    # Create events.
    create_single_threaded_events()
    create_multi_threaded_events()

    # Single threaded finish time.
    single_start = time()
    bus.emit(SINGLE_THREADED, 25)
    single_finish_time = time() - single_start

    multi_start = time()
    bus.emit(MULTI_THREADED, 25, threads=True)
    multi_finish_time = time() - multi_start

    assert multi_finish_time < single_finish_time
