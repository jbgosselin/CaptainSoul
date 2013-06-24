# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from twisted.internet.interfaces import IPushProducer


class Producer(object):
    implements(IPushProducer)

    def __init__(self, protocol, path, progressCallback):
        self._protocol = protocol
        self._goal = os.stat(path).st_size
        self._produced = 0
        self._paused = False
        self._percent = 0
        self._progressCallback = progressCallback
        self._file = file(path, 'r')
        progressCallback(0, self._goal)

    def pauseProducing(self):
        self._paused = True

    def resumeProducing(self):
        self._paused = False
        while not self._paused and self._produced < self._goal:
            data = self._file.read(1024)
            self._protocol.transport.write(data)
            self._produced += len(data)
            if self._produced >= self._goal:
                self._protocol.setAllGood()
            elif 100 * self._produced / self._goal > self._percent:
                self._percent = 100 * self._produced / self._goal
                self._progressCallback(self._produced, self._goal)
        if self._produced == self._goal:
            self._file.close()
            self._protocol.transport.unregisterProducer()
            self._protocol.transport.loseConnection()

    def stopProducing(self):
        self._produced = self._goal
