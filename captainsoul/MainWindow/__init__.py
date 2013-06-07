# -*- coding: utf-8 -*-

import gtk

from ..CmdLine import options
from ..Config import Config
from .. import Icons

from WatchList import WatchList
from ToolBar import ToolBar


class MainWindow(gtk.Window):
    def __init__(self, manager):
        super(MainWindow, self).__init__()
        self.set_properties(title="CaptainSoul", border_width=2, icon=Icons.shield.get_pixbuf())
        self._createUi(manager)
        self.resize(Config['mainWidth'], Config['mainHeight'])
        self.connect("delete-event", self.deleteEvent)
        self.connect("configure-event", self.resizeEvent)
        manager.connect('logged', self.loggedEvent)
        manager.connect('reconnecting', self.reconnectingEvent)
        manager.connect('disconnected', self.disconnectedEvent)
        manager.connect('connecting', self.connectingEvent)
        if not options.tray:
            self.show_all()

    def _createUi(self, manager):
        box = gtk.VBox(False, 0)
        self._toolbar = ToolBar(manager)
        box.pack_start(self._toolbar, False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_size_request(160, 50)
        self._watchlist = WatchList(manager)
        scroll.add_with_viewport(self._watchlist)
        box.pack_start(scroll, True, True, 0)
        self._status = gtk.Statusbar()
        box.pack_start(self._status, False, False, 0)
        self._status.push(0, "Welcome")
        self.add(box)

    # Events

    def resizeEvent(self, *args, **kwargs):
        Config['mainWidth'], Config['mainHeight'] = self.get_size()

    def deleteEvent(self, *args, **kwargs):
        self.hide()
        return True

    def connectingEvent(self, *args, **kwargs):
        self._status.push(0, "Connecting...")

    def showHideEvent(self, *args, **kwargs):
        if self.get_visible():
            self.hide()
        else:
            self.show_all()

    def loggedEvent(self, widget):
        self._status.push(0, "Connected")

    def reconnectingEvent(self, widget):
        self._status.push(0, "Reconnecting...")

    def disconnectedEvent(self, widget):
        self._status.push(0, "Disconnected")
