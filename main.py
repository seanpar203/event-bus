from event_bus import EventBus

eb = EventBus()

@eb.on(event="2", is_same_thread=False)
def a(d=1):
    
    print(d)

if __name__ == '__main__':
    eb.add_event(a, "1")
    eb.emit("1")
    eb.emit("2", "3")
