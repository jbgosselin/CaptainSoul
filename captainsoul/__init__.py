# -*- coding: utf-8 -*-

from twisted.internet import gtk3reactor
gtk3reactor.install()
from twisted.internet import reactor

from gi.repository import Notify
Notify.init("CaptainSoul")

import logging

from CmdLine import options

from Manager import Manager


def configLogging():
    fmt = '%(levelname)s\t: %(message)s'
    level = logging.WARNING
    if options.log_debug:
        level = logging.DEBUG
    elif options.log_info:
        level = logging.INFO
    logging.basicConfig(level=level, format=fmt)


def main():
    configLogging()
    manager = Manager()
    id(manager)
    reactor.run()
