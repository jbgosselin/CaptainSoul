# -*- coding: utf-8 -*-

import logging

import gtk
try:
    import pynotify
except ImportError:
    pynotify = None
from glib import GError

import Icons


class Systray(gtk.StatusIcon):
    def __init__(self, manager, mw):
        super(Systray, self).__init__()
        self.set_from_pixbuf(Icons.shield.get_pixbuf())
        self.set_tooltip_text("CaptainSoul")
        self.set_visible(True)
        self.connect("activate", mw.showHideEvent)
        manager.connect('msg', self.notifyMessage)

    def notifyMessage(self, widget, info, msg, dests):
        if pynotify is not None:
            notif = pynotify.Notification("New message from %s" % info.login, msg, 'dialog-information')
            notif.set_timeout(5000)
            try:
                notif.show()
            except GError:
                logging.warning('Systray : Notification fail')
