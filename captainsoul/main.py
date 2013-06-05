# -*- coding: utf-8 -*-

import CmdLine
CmdLine._void()


def start():
    from twisted.internet import gtk3reactor
    gtk3reactor.install()
    from twisted.internet import reactor
    from MainWindow import MainWindow
    from gi.repository import Notify
    Notify.init("CaptainSoul")
    win = MainWindow()
    id(win)
    reactor.run()
