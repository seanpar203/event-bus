# Event Bus
A simple `Python 3.5+` event bus.


# Purpose
A way to trigger multiple subsequent functions.


# Design choices
In a lot of methods I require passing in a string for the `func_name` parameter.
 
I decided to do this to *not* require users to import the subscribed events into the file.


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


# Real world usage
Here are some examples on real world usage.

```python
from event_bus import EventBus

bus = EventBus()

# Mock Database. 
USERS = {
    1: {
        'name': 'Ricky Bobby',
        'email': 'someuser@gmail.com',
    }
 }


@bus.on(event='new:user')
def send_welcome_email(user_id):
     user = USERS.get(user_id)
     
     # Logic for sending email...
     print('Sent welcome email to {}'.format(user['name']))

@bus.on(event='new:user')
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
from event_bus import EventBus

bus = EventBus()


@bus.on(event='update:ratings:avg')
def update_avg_ratings():
    # Update avg ratings in DB...
    print("Finished updating ratings.")

@bus.emit_after(event='update:ratings:avg')
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
from event_bus import EventBus

# Constsnts
bus = EventBus()
EVENT_NAME = 'event'
GLOBAL_VAR = 'var_1'


# Lets create 2 events subscribed to the same event.
# The last event is the control and shouldn't run with emit_only

@bus.on(event=EVENT_NAME)
def event_one(param):
    global GLOBAL_VAR
    GLOBAL_VAR = param


@bus.on(event=EVENT_NAME)
def event_two(param):
    global GLOBAL_VAR
    GLOBAL_VAR = param


def some_func():
    bus.emit_only(EVENT_NAME, 'event_one', 'it works!')

>>> some_func()    
>>> print(GLOBAL_VAR)
'it works!'
```

# Removing subscribed events.
For some reason you might want to completely remove a subscribed event.

This can be achieved with the method `remove_event(event: str, func_name: str)`

**Note: This can also raise a `EventDoestExist` exception.**

```python
from event_bus import EventBus
from event_bus.exceptions import EventDoesntExist
# Constants.
bus = EventBus()
EVENT_NAME = 'event'


@bus.on(event=EVENT_NAME)
def event_one():
    """ Mock event. """
    pass


def some_func():
    try:
        bus.remove_event(event=EVENT_NAME, func_name='event_one')
    except EventDoesntExist:
        # Handle error here..
        pass
    else:
        print("Removed event.")
    


# This is how you
def another_func():
    

>>> bus.event_count
1
>>> some_func()
"Removed event."
>>> bus.event_count
0
```
