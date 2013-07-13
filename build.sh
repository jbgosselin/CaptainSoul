#!/bin/sh

cd src
zip -r ../cptsoul.zip *.py chatwindow/*.py config/*.py debugwindow/*.py downloadmanager/*.py getfile/*.py Icons/*.py mainwindow/*.py netsoul/*.py sendfile/*.py
cd ..
echo '#!/usr/bin/env python2.7' | cat - cptsoul.zip > cptsoul
chmod +x cptsoul
rm cptsoul.zip
