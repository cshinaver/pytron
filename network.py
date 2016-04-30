#!/usr/bin/python
# network.py

from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.internet import reactor

from event_manager import BeginGameEvent


class ClientProtocol(Protocol):
    def connectionMade(self):
        self.transport.write("waddup betchez")


class ClientConnectionFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ClientProtocol()


class ServerProtocol(Protocol):
    def __init__(self, ev):
        self.event_manager = ev

    def connectionMade(self):
        self.event_manager.post(BeginGameEvent())


class ServerConnectionFactory(Factory):
    def __init__(self, ev):
        self.event_manager = ev

    def buildProtocol(self, addr):
        return ServerProtocol(self.event_manager)


def begin_on_client_connect(ev):
    reactor.listenTCP(40000, ServerConnectionFactory(ev))


if __name__ == '__main__':
    reactor.run()
