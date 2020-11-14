#!/bin/sh
git pull
rm -rf build dist
pyinstaller -F server.py $(ls *.py | grep -v server.py | xargs)
#--hidden-import=gunicorn.glogging     --hidden-import=gunicorn.workers.sync

cd ./dist

[[ -d dmonitor ]] && rm -rf dmonitor

mkdir dmonitor

cp -r ../static dmonitor/
mv server dmonitor/

mkdir dmonitor/config
cp ../config/*.json dmonitor/config
cp ../config/*.yaml dmonitor/config

tar zcvf dmonitor.tgz dmonitor
