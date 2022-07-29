# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Pine
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import re
import threading
import time

import psutil
from flask import (Flask, Response, escape, jsonify, redirect, request,
                   session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer

from app.cron import shutdown, start
from app.metric.api import DataProcessor
from app.metric.helper import list_process_detail_csv
from app.util.logger import log

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
user_socket_list = []


@app.route('/orange')
def orange():
    user_socket = request.environ.get('wsgi.websocket')
    log.info('request %s', request)
    log.info('user_socket %s', user_socket)
    if user_socket:
        user_socket_list.append(user_socket)
        log.info('user_socket_list depth %s', len(user_socket_list))
    while True:
        try:
            msg = user_socket.receive()
            log.info('received: %s', msg)
            for sock in user_socket_list:
                try:
                    sock.send('received: %s' + msg)
                except:
                    continue
        except Exception as e:
            log.error(e)
            if user_socket and user_socket in user_socket_list:
                user_socket_list.remove(user_socket)
            return ''


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/query_monprocess')
def query_monprocess():
    return jsonify(DataProcessor.query_monprocess())


@app.route('/insert_monprocess')
def insert_monprocess():
    parm = request.args.to_dict()
    log.info(parm)
    DataProcessor.insert_monprocess(parm)
    return {'code': 1, 'msg': 'success'}


@app.route('/query_process')
def query_process():
    return list_process_detail_csv()


@app.route('/query_process_by_key_words')
def query_process_by_key_words():
    parm = request.args.to_dict()
    return DataProcessor.query_process_by_key_words(parm)


@app.route('/query_process_full')
def query_process__full():
    resp = []
    for p in psutil.process_iter():
        j = p.as_dict()
        resp.append(j)
    return json.dumps(resp, indent=2)


@app.route('/query_range')
def query_range():
    parm = request.args.to_dict()
    processfilter = parm.get('processfilter')
    wildcard = ''
    if processfilter != '':
        wildcard = re.sub(',', "','", "'"+processfilter+"'")
    log.warn(wildcard)
    start = parm.get('start')
    now = time.time()
    if start is None:
        start = now - 300
    end = parm.get('end')
    if end is None:
        end = now
    return {"data":DataProcessor.query(start, end, wildcard)}


if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=start, args=())
    scheduler_thread.setDaemon(True)
    scheduler_thread.start()
    log.info(u'Scheduler Started.')
    srv = WSGIServer(('0.0.0.0', 8088),
                     app,
                     handler_class=WebSocketHandler,
                     log=log)
    log.info(u'Started Server.')
    srv.serve_forever()
    shutdown()
