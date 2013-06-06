# -*- coding: utf-8 -*-

import logging

from gi.repository import Gtk, Notify
from gi._glib._glib import GError

from .. import Icons


class Systray(Gtk.StatusIcon):
    def __init__(self, mw):
        super(Systray, self).__init__(pixbuf=Icons.shield.get_pixbuf(), tooltip_text="CaptainSoul", visible=True)
        self.connect("activate", mw.showHideEvent)

    def notifyMessage(self, who, msg):
        notif = Notify.Notification.new("New message from %s" % who, msg, 'dialog-information')
        notif.set_timeout(5000)
        try:
            notif.show()
        except GError:
            logging.warning('Systray : Notification fail')
