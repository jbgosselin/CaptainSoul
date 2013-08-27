# -*- coding: utf-8 -*-

from twisted.internet import reactor

from factory import SendFactory


def sendFile(path, ip, port, progCallback, endCallback, errCallback):
    reactor.connectTCP(ip, port, SendFactory(path, progCallback, endCallback, errCallback))
