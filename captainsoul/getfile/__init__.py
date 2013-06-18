# -*- coding: utf-8 -*-

import logging
from os import unlink

from twisted.internet import reactor

from captainsoul.getfile.factory import GetFileFactory


class FileGetter(object):
    def __init__(self, manager, info, name, path, size, proCall, endCall, errorCall):
        self._ok = False
        self._path = path
        self._file = None
        self._endCall = endCall
        self._proCall = proCall
        self._errorCall = errorCall
        self._done = 0
        self._sizeTotal = size
        self._percent = 0
        factory = GetFileFactory(
            self.clientConnectionMade,
            self.clientProgress,
            self.clientConnectionEnd
        )
        self._port = reactor.listenTCP(0, factory)
        logging.info('GetFile : Listen on port %d' % self._port.getHost().port)
        manager.sendFileStart(name, self.get_ip_address()[0], self._port.getHost().port, [info.login])

    def get_ip_address(self):
        import subprocess
        p = subprocess.Popen('ip route list', shell=True, stdout=subprocess.PIPE)
        data = p.communicate()
        sdata = data[0].split()
        ipaddr = sdata[sdata.index('src') + 1]
        netdev = sdata[sdata.index('dev') + 1]
        return ipaddr, netdev

    def clientConnectionMade(self):
        logging.info('GetFile : Client connected')
        self._file = open(self._path, 'w')
        self._port.stopListening()

    def clientProgress(self, data, protocol):
        self._file.write(data)
        self._done += len(data)
        tmp = 100 * self._done / self._sizeTotal
        if tmp > self._percent:
            self._proCall(self._done, self._sizeTotal)
            self._percent = tmp
        if self._done >= self._sizeTotal:
            logging.info('GetFile : Transfer success')
            self._ok = True
            self._file.close()
            protocol.transport.loseConnection()
            self._endCall()

    def clientConnectionEnd(self):
        if not self._ok:
            logging.warning('GetFile : Tranfer aborted')
            self._file.close()
            unlink(self._path)
            self._errorCall()
