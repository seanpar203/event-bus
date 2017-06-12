# Event Bus
<a href="https://travis-ci.org/seanpar203/event-bus"><img src="https://travis-ci.org/seanpar203/event-bus.svg?branch=master" alt="Build Status"></a>


A simple `Python 3.5+` event bus.


# Purpose
A way to trigger multiple subsequent functions.


# Usage
The EventBus is meant to be a singleton used throughout an application.

```python
from event_bus import EventBus

bus = EventBus()

@bus.on('hello')
def subscribed_event():
    print('World!')

def some_func():
    print('Hello')
    bus.emit('hello')

>>> some_func()
"Hello"
"World!"
```

# Performance.
After building the library I started to think about performance and created tests
for multiple scenarios. You can learn exactly what each test is doing by looking
at the `performance_testing.py` file inside the `tests/` directory.

Below are some metrics under 3 different scenarios:

* CPU Heavy(Fibonacci sequence.)
* IO Heavy(30 File reads, loading json.)
* Network Heavy(100 GET requests to a website.)

![](https://github.com/seanpar203/event-bus/blob/master/performance_tests.png)

Because of the results of the tests I decided to add `threading` to the library.
passing `threading=True` in the `emit(event, *args, **kwargs)` method will run
the code using multi-threading, this can significantly speed up the events.


# Design choices
In some of the methods I require passing in a string for the `func_name` parameter.
 
I decided to do this to *not* require users to import the subscribed events into the file.

In that case it would've been better to just call the functions if they're already imported.


# Real world usage
Here are some examples on real world usage.

```python
# Mock Database. 
USERS = {
    1: {
        'name': 'Ricky Bobby',
        'email': 'someuser@gmail.com',
    }
 }


@bus.on('new:user')
def send_welcome_email(user_id):
     user = USERS.get(user_id)

     # Logic for sending email...
     print('Sent welcome email to {}'.format(user['name']))

@bus.on('new:user')
def send_temporary_pass(user_id):
    user = USERS.get(user_id)
    
    # Logic for sending temp pass email...
    print('Sent temp pass email to {}'.format(user['name']))

def create_user():
    # Logic for creating a user...
    user_id = 1
    bus.emit('new:user', user_id)

>>> create_user()
'Sent welcome email to Ricky Bobby'
'Sent temp pass email to Ricky Bobby'
```

# Emitting events after
There is a decorator for emitting events after code completion.

This is great for functions that are standalone.

**`Note: This way doesnt allow the passing of args and kwargs into the events.`**

```python
@bus.on('update:ratings:avg')
def update_avg_ratings():
    # Update avg ratings in DB...
    print("Finished updating ratings.")

@bus.emit_after('update:ratings:avg')
def add_rating():
    # Creating a new rating...
    print("Added new rating.")
    
>>> add_rating()
"Added new rating."
"Finished updating ratings."
```

# Emitting specific events
There might be times when you don't want to emit all the functions that are subscribed to an event.


The `emit_only(event: str, func_names: Union[str, List[str]], *args, **kwargs)` method allows this.
 
The code below is an example.
```python
GLOBAL_VAR = 'var_1'

@bus.on('event')
def event_one(param):
    global GLOBAL_VAR
    GLOBAL_VAR = param


@bus.on('event')
def event_two(param):
    global GLOBAL_VAR
    GLOBAL_VAR = "I don't get called."


def some_func():
    bus.emit_only('event', 'event_one', 'it works!')

>>> some_func()
>>> print(GLOBAL_VAR)
'it works!'
```

# Removing subscribed events.
For some reason you might want to completely remove a subscribed event.

This can be achieved with the method `remove_event(event: str, func_name: str)`

**Note: This can also raise a `EventDoesntExist` exception.**

```python
from event_bus.exceptions import EventDoesntExist

@bus.on('fake_event')
def event_one():
    pass

def some_func():
    try:
        bus.remove_event('fake_event', 'event_one')
    except EventDoesntExist:
        # Handle error here..
        pass
    else:
        print("Removed event.")

>>> bus.event_count
1
>>> some_func()
"Removed event."
>>> bus.event_count
0
```
