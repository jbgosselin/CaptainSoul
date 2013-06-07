# -*- coding: utf-8 -*-

import gtk

from ..CmdLine import options
from ..Config import Config
from .. import Icons

from WatchList import WatchList
from ToolBar import ToolBar
from MainStatus import MainStatus


class MainWindow(gtk.Window):
    def __init__(self, manager):
        super(MainWindow, self).__init__()
        self.set_properties(title="CaptainSoul", border_width=2, icon=Icons.shield.get_pixbuf())
        self._createUi(manager)
        self.resize(Config['mainWidth'], Config['mainHeight'])
        self.connect("delete-event", self.deleteEvent)
        self.connect("configure-event", self.resizeEvent)
        if not options.tray:
            self.show_all()

    def _createUi(self, manager):
        box = gtk.VBox(False, 0)
        box.pack_start(ToolBar(manager), False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_size_request(160, 50)
        scroll.add_with_viewport(WatchList(manager))
        box.pack_start(scroll, True, True, 0)
        box.pack_start(MainStatus(manager), False, False, 0)
        self.add(box)

    # Events

    def resizeEvent(self, *args, **kwargs):
        Config['mainWidth'], Config['mainHeight'] = self.get_size()

    def deleteEvent(self, *args, **kwargs):
        self.hide()
        return True

    def showHideEvent(self, *args, **kwargs):
        if self.get_visible():
            self.hide()
        else:
            self.show_all()
