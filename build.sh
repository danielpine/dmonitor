#!/bin/sh

rm -rf build dist
pyinstaller -F server.py    --hidden-import=gunicorn.glogging     --hidden-import=gunicorn.workers.sync
