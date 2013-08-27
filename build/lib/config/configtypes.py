# -*- coding: utf-8 -*-


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
