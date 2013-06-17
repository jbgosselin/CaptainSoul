# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from captainsoul.Config import createConfigFile


def _get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose', help='Set verbose mode', default=0)
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    parser.add_argument('-d', action='store_true', dest='debug', help='Start with debug window')
    return parser.parse_args()


class CptCommon(object):
    manager = None
    downloadManager = None
    mainWindow = None
    cmdline = _get_args()
    config = createConfigFile()


class PreparedCaller(object):
    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs.update(self._kwargs)
        self._function(*(self._args + args), **kwargs)
