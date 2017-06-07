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
