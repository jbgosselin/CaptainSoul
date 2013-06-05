# -*- coding: utf-8 -*-

import os
import platform
import atexit
from json import load, dump

from ConfigTypes import nonEmptyStrJSON, boolJSON, intJSON, nonEmptyStrSetJSON

__all__ = ['ConfigFile']


def getPath():
    if platform.system() == 'Linux':
        directory = os.path.expanduser('~/.config')
    else:
        directory = './'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, 'cptsoul.json')


class ConfigFile(object):
    '''
    Represent the config file
    Setting the var will alter the config file
    '''
    _data = {}
    _path = getPath()

    def __init__(self):
        keys = [
            ('login', nonEmptyStrJSON, "login"),
            ('password', nonEmptyStrJSON, "password"),
            ('location', nonEmptyStrJSON, "CaptainSoul"),
            ('autoConnect', boolJSON, False),
            ('mainHeight', intJSON, 200),
            ('mainWidth', intJSON, 200),
            ('watchlist', nonEmptyStrSetJSON, set())]
        try:
            data = load(file(self._path, 'r'))
            if not isinstance(data, dict):
                data = {}
        except (IOError, ValueError):
            data = {}
        self._data = {key: klass(data.get(key, default)) for key, klass, default in keys}
        atexit.register(self._atexit)

    def _atexit(self):
        dump({key: value._toJSON() for key, value in self._data.iteritems()}, file(self._path, 'w'))

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]._get()
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key]._set(value)
        else:
            raise KeyError(key)
