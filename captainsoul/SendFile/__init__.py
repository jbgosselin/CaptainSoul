# -*- coding: utf-8 -*-

from twisted.internet import reactor

from Factory import SendFactory


def sendFile(path, ip, port):
    reactor.connectTCP(ip, port, SendFactory(path))
