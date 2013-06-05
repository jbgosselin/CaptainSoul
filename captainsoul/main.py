# -*- coding: utf-8 -*-

from twisted.internet import gtk3reactor
gtk3reactor.install()
from twisted.internet import reactor

from gi.repository import Notify
Notify.init("CaptainSoul")

import logging

from CmdLine import options

from MainWindow import MainWindow


def configLogging():
    fmt = '%(levelname)s:%(message)s'
    level = logging.WARNING
    if options.log_debug:
        level = logging.DEBUG
    elif options.log_info:
        level = logging.INFO
    logging.basicConfig(level=level, format=fmt)


def start():
    configLogging()
    win = MainWindow()
    id(win)
    reactor.run()
