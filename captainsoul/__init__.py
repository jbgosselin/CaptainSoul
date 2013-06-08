# -*- coding: utf-8 -*-

from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor

from CmdLine import options
import logging


def configLogging():
    fmt = '%(levelname)s\t: %(message)s'
    level = logging.WARNING
    if options.verbose >= 2:
        level = logging.DEBUG
    elif options.verbose == 1:
        level = logging.INFO
    logging.basicConfig(level=level, format=fmt)
configLogging()

try:
    import pynotify
    pynotify.init("CaptainSoul")
except ImportError:
    logging.warning('Init : pynotify is not installed')

from Manager import Manager


def main():
    manager = Manager()
    id(manager)
    reactor.run()
