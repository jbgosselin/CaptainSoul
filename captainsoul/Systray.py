# -*- coding: utf-8 -*-

import logging

import gtk
try:
    import pynotify
except ImportError:
    pynotify = None
from glib import GError

import Icons
from Config import Config
from CptCommon import CptCommon


class Systray(gtk.StatusIcon, CptCommon):
    def __init__(self, mw):
        super(Systray, self).__init__()
        self._reconnecting = False
        self.set_from_pixbuf(Icons.shield.get_pixbuf())
        self.set_properties(
            tooltip_text="CaptainSoul",
            visible=True
        )
        self.connect("activate", mw.showHideEvent)
        self.manager.connect('msg', self.msgEvent)
        self.manager.connect('logged', self.loggedEvent)
        self.manager.connect('reconnecting', self.reconnectingEvent)

    def doNotify(self, head, body, img, timeout):
        if pynotify is not None and Config["notification"]:
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
