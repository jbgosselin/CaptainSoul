# -*- coding: utf-8 -*-


class PreparedCaller(object):
    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs.update(self._kwargs)
        self._function(*(self._args + args), **kwargs)
