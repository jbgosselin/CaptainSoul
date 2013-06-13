# -*- coding: utf-8 -*-

import gtk

from .. import Icons
from tools import sizeFormatter


class AskFileWindow(gtk.Window):
    def __init__(self, manager, info, name, size, desc):
        super(AskFileWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul - File request",
            icon=Icons.shield.get_pixbuf(),
            resizable=False
        )
        self._createUi(manager, info, name, size)
        self.show_all()

    def _createUi(self, manager, info, name, size):
        box = gtk.VBox(False, 0)
        self.add(box)
        box.pack_start(gtk.Label('%s want to send you a file' % info.login), False, False)
        box.pack_start(gtk.Label(name), False, False)
        box.pack_start(gtk.Label(sizeFormatter(size)), False, False)
        bbox = gtk.HButtonBox()
        box.pack_start(bbox)
        baccept = gtk.Button(label='Accept', stock=gtk.STOCK_YES)
        bbox.add(baccept)
        baccept.connect('clicked', self.acceptFileEvent, manager, info, name, size)
        brefuse = gtk.Button(label='Refuse', stock=gtk.STOCK_NO)
        bbox.add(brefuse)
        brefuse.connect('clicked', self.refuseFileEvent)

    def acceptFileEvent(self, widget, manager, info, name, size):
        dialog = gtk.FileChooserDialog(
            title='CatpainSoul - Choose destination',
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=('Ok', gtk.RESPONSE_OK, 'Cancel', gtk.RESPONSE_CANCEL)
        )
        dialog.set_current_name(name)
        if dialog.run() != gtk.RESPONSE_OK:
            dialog.destroy()
            self.destroy()
        else:
            path = dialog.get_filename()
            dialog.destroy()
            manager.startFileDownload(info, name, size, path)
            self.destroy()

    def refuseFileEvent(self, widget):
        self.destroy()
