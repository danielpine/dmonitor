#!/bin/sh
git pull
rm -rf build dist
pyinstaller -F server.py `ls *.py | grep -v server.py | xargs`   
#--hidden-import=gunicorn.glogging     --hidden-import=gunicorn.workers.sync
