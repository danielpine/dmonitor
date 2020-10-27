#!/bin/sh
git pull
rm -rf build dist
pyinstaller -F server.py `ls *.py | grep -v server.py | xargs`   
#--hidden-import=gunicorn.glogging     --hidden-import=gunicorn.workers.sync

cd ./dist 
mkdir dmonitor
cp server dmonitor/
cp -r ../static dmonitor/
tar zcvf dmonitor.tgz dmonitor
rm -rf dmonitor
