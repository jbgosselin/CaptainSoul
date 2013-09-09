# -*- coding: utf-8 -*-

import os
import platform
import user

from cptsoul.config.configfile import ConfigFile


def createConfigFile():
    if platform.system() == 'Linux':
        directory = os.path.join(user.home, '.config')
    elif platform.system() == 'Windows':
        directory = os.path.join(os.getenv('APPDATA'), 'Roaming')
    else:
        directory = './'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return ConfigFile(os.path.join(directory, 'cptsoul.json'))
