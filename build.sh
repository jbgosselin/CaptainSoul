#!/bin/sh

NAME="cptsoul"

cd src
echo "Building pyo"
for f in `find . -name '*.py'`
do
    python2.7 -OO -m py_compile $f
done
echo "Building executable"
zip -q -9 -r "../$NAME.zip" `find . -name '*.pyo'`
cd ..
echo '#!/usr/bin/env python2.7' | cat - "$NAME.zip" > "$NAME"
chmod +x "$NAME"
rm "$NAME".zip
echo "Building done"
