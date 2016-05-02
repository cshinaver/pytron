#!/usr/bin/python
# network.py

import logging
import pickle

from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from event_manager import (
    BeginGameEvent,
    RegisterPlayerEvent,
    LocalMoveCharactorEvent,
    RemoteMoveCharactorEvent,
    PlayerSetIDEvent,
    CheckinEvent,
    RemoteMovePlayer,
    LocalMovePlayer,
)


class ClientProtocol(LineReceiver):
    def __init__(self, ev):
        self.event_manager = ev
        self.event_manager.register_listener(self)

    def connectionMade(self):
        logging.info('Connection made to server')
        self.transport.write(pickle.dumps(CheckinEvent()) + '\r\n')

    def lineReceived(self, data):
        e = pickle.loads(data)
        logging.info('Decoded server data: {e}'.format(e=e))
        logging.info('Posting received event: {e}'.format(
            e=e.__class__.__name__,
        ))
        self.event_manager.post(e)

    def notify(self, event):
        if isinstance(event, LocalMoveCharactorEvent):
            r = RemoteMoveCharactorEvent(event.id, event.direction)
            self.transport.write(pickle.dumps(r) + '\r\n')
        elif isinstance(event, LocalMovePlayer):
            r = RemoteMovePlayer(event.id, event.x, event.y)
            self.transport.write(pickle.dumps(r) + '\r\n')


class ClientConnectionFactory(ClientFactory):
    def __init__(self, ev):
        self.event_manager = ev

    def buildProtocol(self, addr):
        return ClientProtocol(self.event_manager)


class ServerProtocol(LineReceiver):
    def __init__(self, ev):
        self.event_manager = ev
        self.event_manager.register_listener(self)

    def connectionMade(self):
        logging.info(
            'Connection received from {c}'.format(
                c=self.transport.client
            )
        )

    def lineReceived(self, data):
        self.event_manager.post(pickle.loads(data))

    def notify(self, event):
        if isinstance(event, LocalMoveCharactorEvent):
            r = RemoteMoveCharactorEvent(event.id, event.direction)
            self.transport.write(pickle.dumps(r) + '\r\n')
        elif isinstance(event, LocalMovePlayer):
            r = RemoteMovePlayer(event.id, event.x, event.y)
            self.transport.write(pickle.dumps(r) + '\r\n')
        elif isinstance(event, CheckinEvent):
            id = 1
            x = 200
            y = 200
            p1 = RegisterPlayerEvent(id, x, y)
            p2 = RegisterPlayerEvent(id + 1, 400, 400)
            logging.info('Broadcasting host player {id}'.format(id=id))
            self.transport.write(pickle.dumps(p1) + '\r\n')
            self.event_manager.post(p1)
            self.event_manager.post(PlayerSetIDEvent(p1.id))

            logging.info('Sending player {id} info'.format(id=p2.id))
            self.transport.write(pickle.dumps(p2) + '\r\n')
            self.transport.write(
                pickle.dumps(PlayerSetIDEvent(p2.id)) + '\r\n',
            )
            self.event_manager.post(p2)

            logging.info('Sending BeginGameEvent to clients')
            self.transport.write(pickle.dumps(BeginGameEvent()) + '\r\n')
            logging.info('Posting BeginGameEvent')
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
