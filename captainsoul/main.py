# -*- coding: utf-8 -*-

from twisted.internet import gtk3reactor
gtk3reactor.install()
from twisted.internet import reactor

from gi.repository import Notify
Notify.init("CaptainSoul")

from MainWindow import MainWindow


def start():
    win = MainWindow()
    id(win)
    reactor.run()
