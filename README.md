# Event Bus
A simple `Python 3.5+` event bus.


# Purpose
A way to trigger multiple subsequent functions.


# Usage
The EventBus is meant to be a singleton used throughout an application.

```python
from event_bus import EventBus


bus = EventBus() 


@bus.on(event='hello')
def subscribed_event():
    print('Hello World')


def some_func():
    # Some real application logic would go here.
    bus.emit(event='hello')

>>> some_func()
'Hello World'
```
