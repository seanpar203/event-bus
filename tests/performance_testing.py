""" Tests performance of executing multiple functions. """
# Modules
import json
import requests
from os import getcwd
from timeit import default_timer as timer
from threading import Thread
from multiprocessing import Process

# Libs
from event_bus import EventBus

bus = EventBus()
EVENT_ONE = 'test_1'
EVENT_TWO = 'test_2'
EVENT_THREE = 'test_3'


# -----------------------------------------------------------------------------

# ------------------------------------------
# CPU Heavy Tests
# ------------------------------------------

def create_event_one():
    for i in range(10):
        @bus.on(event=EVENT_ONE)
        def fib(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fib(n - 1) + fib(n - 2)


print(
    "\n"
    "CPU Heavy Tests:"
    "\n"
)

create_event_one()

# ------------------------------------------
# Single Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Single-threaded'

start = timer()

bus.emit(EVENT_ONE, 30)

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-threaded'

start = timer()

events = [Thread(target=func, args=[30]) for func in bus._events[EVENT_ONE]]
for func in events:
    func.start()

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-process Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-process'

start = timer()

events = [Process(target=func, args=[30]) for func in bus._events[EVENT_ONE]]
for func in events:
    func.start()

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))


# -----------------------------------------------------------------------------

# ------------------------------------------
# IO Heavy Tests
# ------------------------------------------

def create_event_two():
    for i in range(30):
        @bus.on(event=EVENT_TWO)
        def read_file():
            with open('{}/generated.json'.format(getcwd())) as f:
                data = json.load(f)


print(
    "\n"
    "IO Heavy Tests:"
    "\n"
)

create_event_two()
# ------------------------------------------
# Single Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Single-threaded'

start = timer()

bus.emit(EVENT_TWO)

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-threaded'

start = timer()

events = [Thread(target=func) for func in bus._events[EVENT_TWO]]
for func in events:
    func.start()

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-process Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-process'

start = timer()

events = [Process(target=func) for func in bus._events[EVENT_TWO]]
for func in events:
    func.start()

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))


# -----------------------------------------------------------------------------

# ------------------------------------------
# Network Heavy Tests
# ------------------------------------------

def create_event_three():
    for i in range(100):
        @bus.on(event=EVENT_THREE)
        def get_url():
            response = requests.get(
                'http://marvel.wikia.com/wiki/Marvel_Database')


print(
    "\n"
    "Network Heavy Tests:"
    "\n"
)

create_event_three()
# ------------------------------------------
# Single Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Single-threaded'

start = timer()

bus.emit(EVENT_THREE)

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-threaded'

start = timer()

events = [Thread(target=func) for func in bus._events[EVENT_THREE]]
for func in events:
    func.start()

finish = timer() - start
print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-process Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-process'

start = timer()

events = [Process(target=func) for func in bus._events[EVENT_THREE]]
for func in events:
    func.start()

finish = timer() - start

print("{} ran the code in {} seconds.".format(TEST_TYPE, finish))
