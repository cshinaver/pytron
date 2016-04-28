#!/usr/bin/python
# event_manager.py


class TickEvent:
    pass


class QuitGameEvent:
    pass


class EventManager:
    def __init__(self):
        self.listeners = {}

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        del self.listeners[listener]

    def post(self, event):
        for listener in self.listeners.keys():
            listener.notify(event)
