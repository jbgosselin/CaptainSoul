#!/usr/bin/env python2.7

from distutils.sysconfig import get_python_lib
import os
import shutil

if __name__ == "__main__":
    d = os.path.join(get_python_lib(), "captainsoul")
    if os.path.exists(d):
        shutil.rmtree(d)
