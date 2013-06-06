# -*- coding: utf-8 -*-

from gi.repository import Gtk, Notify

from .. import Icons


class Systray(Gtk.StatusIcon):
    def __init__(self, mw):
        super(Systray, self).__init__(pixbuf=Icons.shield.get_pixbuf(), tooltip_text="CaptainSoul", visible=True)
        self.connect("activate", mw.showHideEvent)

    def notifyMessage(self, who, msg):
        notif = Notify.Notification.new("New message from %s" % who, msg, 'dialog-information')
        notif.set_timeout(5000)
        notif.show()
