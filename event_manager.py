#!/usr/bin/python
# event_manager.py


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


class MoveCharactorEvent:
    def __init__(self, direction):
        self.direction = direction


class TickEvent:
    pass


class QuitGameEvent:
    pass


class BeginGameEvent:
    pass


class RegisterPlayerEvent:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class PlayerSetIDEvent:
    def __init__(self, id):
        self.id = id
