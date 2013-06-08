#!/bin/sh

./setup.py build && sudo ./remove.py && sudo ./setup.py install --optimize=2
