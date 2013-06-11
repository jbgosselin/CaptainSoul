# -*- coding: utf-8 -*-

import logging

from twisted.internet import reactor

from Factory import GetFileFactory


class FileGetter(object):
    def __init__(self, manager, info, name, path, size, proCall, endCall):
        self._path, self._file, self._endCall, self._proCall, self._done, self._sizeTotal = path, None, endCall, proCall, 0, size
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
        self._proCall(self._done, self._sizeTotal)
        if self._done >= self._sizeTotal:
            protocol.transport.loseConnection()

    def clientConnectionEnd(self):
        logging.info('GetFile : Transfer terminated')
        self._file.close()
        self._endCall()
