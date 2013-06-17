# -*- coding: utf-8 -*-

import os
import platform
import user

from captainsoul.Config.ConfigFile import ConfigFile

__all__ = ['Config']


def createConfigFile():
    if platform.system() == 'Linux':
        directory = os.path.join(user.home, '.config')
    else:
        directory = './'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return ConfigFile(os.path.join(directory, 'cptsoul.json'))
Config = createConfigFile()
