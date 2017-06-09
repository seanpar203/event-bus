""" Tests performance of executing multiple functions. """
# Modules
from time import time
from threading import Thread
from multiprocessing import Process

# Libs
from event_bus import EventBus

bus = EventBus()
EVENT_NAME = 'performance.'

for i in range(10):
    @bus.on(event=EVENT_NAME)
    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

print(
    "\n"
    "The testing below tests the code under 3 different circumstances."
    "\n"
)
# ------------------------------------------
# Single Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Single-threaded'

start = time()

bus.emit(EVENT_NAME, 30)

finish = time() - start
print("{} ran the code in {}".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-Threaded Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-threaded'

start = time()

events = [Thread(target=func, args=[30]) for func in bus._events[EVENT_NAME]]
for func in events:
    func.start()

finish = time() - start
print("{} ran the code in {}".format(TEST_TYPE, finish))

# ------------------------------------------
# Multi-process Code Execution.
# ------------------------------------------
TEST_TYPE = 'Multi-process'

start = time()

events = [Process(target=func, args=[30]) for func in bus._events[EVENT_NAME]]
for func in events:
    func.start()

finish = time() - start
print("{} ran the code in {}".format(TEST_TYPE, finish))
