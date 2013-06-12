# -*- coding: utf-8 -*-

from twisted.internet.protocol import ClientFactory

from Protocol import SendProtocol


class SendFactory(ClientFactory):
    def __init__(self, path):
        self._path = path

    def buildProtocol(self, addr):
        return SendProtocol(self._path)
