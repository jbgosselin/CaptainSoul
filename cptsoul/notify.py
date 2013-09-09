# -*- coding: utf-8 -*-

import logging
import platform

if platform.system() == 'Linux':
    try:
        import pynotify
    except ImportError:
        pynotify = None
        try:
            import dbus
        except ImportError:
            dbus = None
else:
    pynotify = None
    dbus = None
from glib import GError

from cptsoul.common import CptCommon


class Notifier(CptCommon):
    appName = "CaptainSoul"

    def __init__(self):
        if pynotify is not None:
            pynotify.init(self.appName)
        elif dbus is not None:
            _bus_name = 'org.freedesktop.Notifications'
            _object_path = '/org/freedesktop/Notifications'
            _interface_name = _bus_name
            session_bus = dbus.SessionBus()
            obj = session_bus.get_object(_bus_name, _object_path)
            self._dbus_interface = dbus.Interface(obj, _interface_name)

    def notify(self, head, body, img, timeout=3000):
        if self.config["notification"]:
            if pynotify is not None:
                notif = pynotify.Notification(head, body, img)
                notif.set_timeout(timeout)
                try:
                    notif.show()
                except GError:
                    logging.warning('Systray : Notification fail')
            elif dbus is not None:
                self._dbus_interface.Notify(self.appName, 0, img, head, body, [], [], timeout)
