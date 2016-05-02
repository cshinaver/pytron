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


class TickEvent:
    pass


class QuitGameEvent:
    pass


class BeginGameEvent:
    def __init__(self):
        self.name = 'BeginGameEvent'

    def to_dict(self):
        content = {
            'name': self.name,
        }
        return content


class RegisterPlayerEvent:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class PlayerSetIDEvent:
    def __init__(self, id):
        self.id = id


class CheckinEvent:
    pass


class LocalMoveCharactorEvent:
    def __init__(self, id, direction):
        self.id = id
        self.direction = direction


class RemoteMoveCharactorEvent:
    def __init__(self, id, direction):
        self.id = id
        self.direction = direction


class RemoteMovePlayer:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class LocalMovePlayer:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class PlayerCollision:
    def __init__(self, player_id, object_id):
        self.player_id = player_id
        self.object_id = object_id

class PlayerDeath:
    def __init__(self, id):
        self.id = id

class RemotePlayerDeath:
    def __init__(self, id):
        self.id = id
