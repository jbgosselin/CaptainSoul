# -*- coding: utf-8 -*-

import gtk

from captainsoul.common import CptCommon

from captainsoul.MainWindow.WatchList import WatchList
from captainsoul.MainWindow.ToolBar import ToolBar
from captainsoul.MainWindow.MainStatus import MainStatus


class MainWindow(gtk.Window, CptCommon):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul"
        )
        self.resize(self.config['mainWidth'], self.config['mainHeight'])
        self._createAccels()
        self._createUi()
        self.connect("delete-event", self.hide_on_delete)
        self.connect("configure-event", self.resizeEvent)
        if not self.cmdline.tray:
            self.show_all()

    def _createAccels(self):
        accels = [
            ('<ctrl>p', self.manager.openSettingsWindowEvent),
            ('<ctrl>o', self.manager.openAddContactWindowEvent),
            ('<ctrl>q', self.manager.quitEvent),
            ('Escape', self.hide_on_delete)
        ]
        ag = gtk.AccelGroup()
        self.add_accel_group(ag)
        for accel, callback in accels:
            key, mask = gtk.accelerator_parse(accel)
            ag.connect_group(key, mask, gtk.ACCEL_VISIBLE, callback)

    def _createUi(self):
        box = gtk.VBox(False, 0)
        self.add(box)
        box.pack_start(ToolBar(), False, False, 0)
        scroll = gtk.ScrolledWindow()
        scroll.set_properties(
            hscrollbar_policy=gtk.POLICY_NEVER,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC,
            shadow_type=gtk.SHADOW_ETCHED_IN)
        scroll.add(WatchList())
        box.pack_start(scroll, True, True, 0)
        box.pack_start(MainStatus(), False, False, 0)

    # Events

    def resizeEvent(self, *args, **kwargs):
        self.config['mainWidth'], self.config['mainHeight'] = self.get_size()

    def showHideEvent(self, *args, **kwargs):
        if self.get_visible():
            self.hide()
        else:
            self.show_all()
