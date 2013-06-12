# -*- coding: utf-8 -*-

import gtk

from .. import Icons
from ..Config import Config
from DownloadList import DownloadList


class DownloadManager(gtk.Window):
    def __init__(self, manager):
        super(DownloadManager, self).__init__()
        self.set_properties(
            title="CaptainSoul - Download Manager",
            icon=Icons.shield.get_pixbuf()
        )
        self.resize(Config['downWidth'], Config['downHeight'])
        self._createUi(manager)
        self.connect("delete-event", self.hide_on_delete)
        self.connect("configure-event", self.resizeEvent)

    def _createUi(self, manager):
        box = gtk.VBox(False, 0)
        self.add(box)
        scroll = gtk.ScrolledWindow()
        scroll.set_properties(
            hscrollbar_policy=gtk.POLICY_AUTOMATIC,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC,
            shadow_type=gtk.SHADOW_ETCHED_IN)
        down = DownloadList(self, manager)
        self.startFileDownload = down.startFileTransfer
        scroll.add(down)
        box.pack_start(scroll, True, True, 0)

    def resizeEvent(self, *args, **kwargs):
        Config['downWidth'], Config['downHeight'] = self.get_size()
