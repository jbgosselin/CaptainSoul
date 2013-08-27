from distutils.core import setup
import py2exe
import os
import shutil

def packages():
    p = ['']
    for dirname, dirnames, filenames in os.walk('src'):
        if dirname != 'src':
            dirname = dirname[4:]
            p.append(dirname)
    return p

setup(
    zipfile = None,
    windows = [
        {
            'script': 'src/__main__.py',
        }
    ],
    package_dir = {'': 'src'},
    packages = packages(),
    options = {
        'py2exe': {
            'bundle_files': 3,
            'compressed': True,
            'optimize': 2,
            'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
            'dll_excludes': [
                "mswsock.dll",
                "powrprof.dll"
            ],
        }
    }
)

shutil.move('dist/__main__.exe', 'dist/cptsoul.exe')
