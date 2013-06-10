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
        self.set_properties(title="CaptainSoul", icon=Icons.shield.get_pixbuf())
        self._createAccels(manager)
        self._createUi(manager)
        self.resize(Config['mainWidth'], Config['mainHeight'])
        self.connect("delete-event", self.deleteEvent)
        self.connect("configure-event", self.resizeEvent)
        if not options.tray:
            self.show_all()

    def _createAccels(self, manager):
        accels = [
            ('<ctrl>p', manager.openSettingsWindowEvent),
            ('<ctrl>o', manager.openAddContactWindowEvent),
            ('<ctrl>q', manager.quitEvent),
            ('Escape', self.deleteEvent)
        ]
        ag = gtk.AccelGroup()
        self.add_accel_group(ag)
        for accel, callback in accels:
            key, mask = gtk.accelerator_parse(accel)
            ag.connect_group(key, mask, gtk.ACCEL_VISIBLE, callback)

    def _createUi(self, manager):
        box = gtk.VBox(False, 0)
        self.add(box)
        box.pack_start(ToolBar(manager), False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroll.add(WatchList(manager))
        box.pack_start(scroll, True, True, 0)
        box.pack_start(MainStatus(manager), False, False, 0)

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
