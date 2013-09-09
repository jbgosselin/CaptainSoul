# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
from gtk.gdk import pixbuf_new_from_file


def _createImage(name):
    return pixbuf_new_from_file(resource_filename('cptsoul', 'icons/%s.png' % name))


red = _createImage('red')
green = _createImage('green')
void = _createImage('void')
shield = _createImage('shield')
epitech = _createImage('epitech')
orange = _createImage('orange')
