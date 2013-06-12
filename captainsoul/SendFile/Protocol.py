# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol

from Producer import Producer


class SendProtocol(Protocol):
    def __init__(self, path):
        self._path = path
        self._allGood = False

    def connectionMade(self):
        producer = Producer(self, self._path)
        self.transport.registerProducer(producer, True)
        producer.resumeProducing()

    def connectionLost(self, reason):
        pass

    def setAllGood(self):
        self._allGood = True
