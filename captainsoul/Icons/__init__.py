# -*- coding: utf-8 -*-

from os.path import abspath, join, dirname

import gtk


def _createImage(name):
    image = gtk.Image()
    image.set_from_file(join(dirname(abspath(__file__)), name))
    return image

red = _createImage('red.png')
green = _createImage('green.png')
void = _createImage('void.png')
shield = _createImage('shield.png')
epitech = _createImage('epitech.png')
