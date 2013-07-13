# -*- coding: utf-8 -*-

from gtk.gdk import pixbuf_new_from_inline

import data


def _createImage(raw):
    return pixbuf_new_from_inline(len(raw), raw, False)

red = _createImage(data.raw_red)
green = _createImage(data.raw_green)
void = _createImage(data.raw_void)
shield = _createImage(data.raw_shield)
epitech = _createImage(data.raw_epitech)
orange = _createImage(data.raw_orange)
