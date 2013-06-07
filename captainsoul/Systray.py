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
    _reconnecting = False

    def __init__(self, manager, mw):
        super(Systray, self).__init__()
        self.set_from_pixbuf(Icons.shield.get_pixbuf())
        self.set_tooltip_text("CaptainSoul")
        self.set_visible(True)
        self.connect("activate", mw.showHideEvent)
        manager.connect('msg', self.msgEvent)
        manager.connect('logged', self.loggedEvent)
        manager.connect('reconnecting', self.reconnectingEvent)

    def doNotify(self, head, body, img, timeout):
        if pynotify is not None:
            notif = pynotify.Notification(head, body, img)
            notif.set_timeout(timeout)
            try:
                notif.show()
            except GError:
                logging.warning('Systray : Notification fail')

    def msgEvent(self, widget, info, msg, dests):
        self.doNotify("CaptainSoul - New message from %s" % info.login, msg, 'dialog-information', 5000)

    def loggedEvent(self, widget):
        self._reconnecting = False
        self.doNotify('CaptainSoul', 'Connected', 'dialog-ok', 3000)

    def reconnectingEvent(self, widget):
        if not self._reconnecting:
            self.doNotify('CaptainSoul', 'Connection lost, reconnecting', 'dialog-warning', 3000)
            self._reconnecting = True
