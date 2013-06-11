# -*- coding: utf-8 -*-

import gtk

import Icons


class FileProgressWindow(gtk.Window):
    def __init__(self, info):
        super(FileProgressWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul - Retrieving file from %s" % info.login,
            icon=Icons.shield.get_pixbuf(),
            width_request=200,
            height_request=50
        )
        self._createUi()
        self.show_all()

    def progressCallback(self, current, total):
        frac = current / float(total)
        self._progress.set_fraction(frac)
        self._progress.set_text("Retrieving %d%%" % (frac * 100))

    def endCallback(self):
        self._progress.set_fraction(1)
        self._progress.set_text("Transfer terminated")

    def errorCallback(self):
        self._progress.set_text("Transfer aborted")

    def _createUi(self):
        self._progress = gtk.ProgressBar()
        self._progress.set_text("Waiting for data")
        self.add(self._progress)
