#!/usr/bin/python
# network.py

import logging
import pickle

from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.internet import reactor

from event_manager import (
    BeginGameEvent,
    RegisterPlayerEvent,
    MoveCharactorEvent,
)


class ClientProtocol(Protocol):
    def __init__(self, ev):
        self.event_manager = ev

    def connectionMade(self):
        logging.info('Connection made to server')
        self.transport.write('meh')

    def dataReceived(self, data):
        logging.info('Data received from server: {d}'.format(
            d=data,
        ))
        e = pickle.loads(data)
        logging.info('Decoded server data: {e}'.format(e=e))
        logging.info('Posting received event: {e}'.format(
            e=e.__class__.__name__,
        ))
        self.event_manager.post(e)


class ClientConnectionFactory(ClientFactory):
    def __init__(self, ev):
        self.event_manager = ev

    def buildProtocol(self, addr):
        return ClientProtocol(self.event_manager)


class ServerProtocol(Protocol):
    def __init__(self, ev):
        self.event_manager = ev
        self.event_manager.register_listener(self)

    def connectionMade(self):
        logging.info(
            'Connection received from {c}'.format(
                c=self.transport.client
            )
        )

    def dataReceived(self, data):
        id = 2
        x = 200
        y = 200
        r = RegisterPlayerEvent(id, x, y)
        self.event_manager.post(r)
        logging.info('Sending BeginGameEvent to clients')
        self.transport.write(pickle.dumps(BeginGameEvent()))
        logging.info('Posting BeginGameEvent')
        self.event_manager.post(BeginGameEvent())

    def notify(self, event):
        if isinstance(event, MoveCharactorEvent):
            direction = event.direction
            self.transport.write('{d}'.format(d=direction))


class ServerConnectionFactory(Factory):
    def __init__(self, ev):
        self.event_manager = ev

    def buildProtocol(self, addr):
        return ServerProtocol(self.event_manager)


def begin_on_client_connect(ev, PORT):
    logging.info('Listening on port {p}'.format(p=PORT))
    reactor.listenTCP(PORT, ServerConnectionFactory(ev))


def connect_to_server_host(ev, HOST, PORT):
    logging.info('Connecting to {h}:{p}'.format(h=HOST, p=PORT))
    reactor.connectTCP(HOST, PORT, ClientConnectionFactory(ev))
