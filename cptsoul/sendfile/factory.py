# -*- coding: utf-8 -*-

from twisted.internet.protocol import ClientFactory

from cptsoul.sendfile.protocol import SendProtocol


class SendFactory(ClientFactory):
    def __init__(self, path, progressCallback, endCallback, errorCallback):
        self._path = path
        self._progressCallback = progressCallback
        self._endCallback = endCallback
        self._errorCallback = errorCallback

    def buildProtocol(self, addr):
        return SendProtocol(self._path, self._progressCallback, self._endCallback, self._errorCallback)
