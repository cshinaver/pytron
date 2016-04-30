#!/usr/bin/python
# network.py

import logging

from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.internet import reactor

from event_manager import BeginGameEvent, RegisterPlayerEvent


class ClientProtocol(Protocol):
    def __init__(self, ev):
        self.event_manager = ev

    def connectionMade(self):
        logging.info('Connection made to server')
        self.transport.write('meh')


class ClientConnectionFactory(ClientFactory):
    def __init__(self, ev):
        self.event_manager = ev

    def buildProtocol(self, addr):
        return ClientProtocol(self.event_manager)


class ServerProtocol(Protocol):
    def __init__(self, ev):
        self.event_manager = ev

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
        self.event_manager.post(BeginGameEvent())


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
