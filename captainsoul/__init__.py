# -*- coding: utf-8 -*-

from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor

import logging

from captainsoul.common import CptCommon


def configLogging():
    fmt = '%(levelname)s\t: %(message)s'
    level = logging.WARNING
    if CptCommon.cmdline.verbose >= 2:
        level = logging.DEBUG
    elif CptCommon.cmdline.verbose == 1:
        level = logging.INFO
    logging.basicConfig(level=level, format=fmt)
configLogging()

try:
    import pynotify
    pynotify.init("CaptainSoul")
except ImportError:
    logging.warning('Init : pynotify is not installed')

from captainsoul.manager import Manager


def main():
    manager = Manager()
    id(manager)
    reactor.run()
