# -*- coding: utf-8 -*-

import logging
from json import load, dump

from twisted.internet import reactor

from cptsoul.config.configtypes import nonEmptyStrJSON, boolJSON, intJSON, nonEmptyStrSetJSON


class ConfigFile(object):
    def __init__(self, path):
        self._path = path
        self._data = {}
        self.read()
        reactor.addSystemEventTrigger('before', 'shutdown', self.write)

    def read(self):
        keys = [
            ('login', nonEmptyStrJSON, "login"),
            ('password', nonEmptyStrJSON, "password"),
            ('location', nonEmptyStrJSON, "CaptainSoul"),
            ('autoConnect', boolJSON, False),
            ('notification', boolJSON, True),
            ('lastUpdate', intJSON, 0),
            ('mainHeight', intJSON, 500),
            ('mainWidth', intJSON, 350),
            ('chatHeight', intJSON, 200),
            ('chatWidth', intJSON, 200),
            ('downHeight', intJSON, 200),
            ('downWidth', intJSON, 200),
            ('watchlist', nonEmptyStrSetJSON, set())
        ]
        try:
            data = load(file(self._path, 'r'))
            if not isinstance(data, dict):
                logging.warning("Config : File is not well formatted")
                data = {}
        except IOError:
            logging.warning("Config : File don't exist")
            data = {}
        except ValueError:
            logging.warning("Config : File isn't JSON")
            data = {}
        else:
            logging.info("Config : File ok")
        self._data = {key: klass(data.get(key, default)) for key, klass, default in keys}

    def write(self):
        try:
            dump(
                {key: value._toJSON() for key, value in self._data.iteritems()},
                file(self._path, 'w'),
                indent=4,
                separators=(',', ': ')
            )
        except:
            logging.warning("Config : Can't write file")
        else:
            logging.info("Config : File successfully written")

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
