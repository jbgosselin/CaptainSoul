# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol


class GetFileProtocol(Protocol):
    def __init__(self, coCall, proCall, endCall):
        self._coCall, self._proCall, self._endCall = coCall, proCall, endCall

    def connectionMade(self):
        self._coCall()

    def connectionLost(self, reason):
        self._endCall()

    def dataReceived(self, data):
        self._proCall(data, self)
