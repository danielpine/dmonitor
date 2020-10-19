#!/bin/sh
git pull
rm -rf build dist
pyinstaller -F server.py `ls *.py | grep -v server.py | xargs`   
#--hidden-import=gunicorn.glogging     --hidden-import=gunicorn.workers.sync

cd ./dist 
zip -r dmonitor_`date +%Y%m%d_%H%M%S`.zip server ../static

