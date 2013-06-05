# -*- coding: utf-8 -*-

import os
import platform
import atexit
from json import load, dump


__all__ = ['Config']


class defaultJSON(object):
    def __init__(self, value):
        self._set(value)

    def _get(self):
        return self._value

    def _set(self, value):
        self._value = value

    def _toJSON(self):
        return self._value


class nonEmptyStrSetJSON(defaultJSON):
    def _set(self, value):
        self._value = set([v for v in value if isinstance(v, basestring) if v])

    def _toJSON(self):
        return list(self._value)

    def _get(self):
        return self

    def add(self, v):
        if isinstance(v, basestring) and v:
            self._value.add(v)

    def clear(self):
        self._value.clear()

    def remove(self, v):
        self._value.remove(v)

    def __len__(self):
        return len(self._value)

    def __iter__(self):
        return iter(self._value)

    def __contains__(self, item):
        return self._value.__contains__(item)


class intJSON(defaultJSON):
    def _set(self, value):
        self._value = int(value)


class boolJSON(defaultJSON):
    def _set(self, value):
        self._value = bool(value)


class nonEmptyStrJSON(defaultJSON):
    def _set(self, value):
        if isinstance(value, basestring):
            if len(value) > 0:
                self._value = value
        else:
            raise TypeError("String only")


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
            self._data[name]._set(value)
        else:
            raise KeyError(key)


Config = ConfigFile()
