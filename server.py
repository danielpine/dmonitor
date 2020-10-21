import logging
import threading
import time

from flask import (Flask, Response, escape, jsonify, redirect, request,
                   session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
import psutil

from cron import get_mem_size

from cron import shutdown, start
from data import select_from_record, select_from_record_filter
from logger import log

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
            log.info(e)
            if user_socket and user_socket in user_socket_list:
                user_socket_list.remove(user_socket)
            return ''


@app.route('/')
def index():
    return app.send_static_file('index.html')

def quiet_exec(fun):
        try:
            result=fun()
            log.info(result)
            return result
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return ''

@app.route('/query_process')
def query_process():
    data = []
    title='Pid,Ppid,Name,MemUsed,Cpu_Percent,Cmdline'
    data.append(title)
    for p in psutil.process_iter():
        data.append(','.join([str(e) for e in [ p.pid,p.ppid(), p.name(), get_mem_size(p), p.cpu_percent(),'  '.join(quiet_exec(p.cmdline))]]))
    return '\n'.join(data)
    
@app.route('/query_range')
def query_range():
    parm = request.args.to_dict()
    start = parm.get('start')
    processfilter = parm.get('processfilter')
    now = time.time()
    if start is None:
        start = now - 300
    end = parm.get('end')
    if end is None:
        end = now
    if processfilter and len(processfilter.strip()) > 0:
        return jsonify(select_from_record_filter(start, end, processfilter))
    else:
        return jsonify(select_from_record(start, end))


if __name__ == "__main__":
    logging.getLogger('PokeAlarm').setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.INFO)
    logging.getLogger('pyswgi').setLevel(logging.INFO)
    logging.getLogger('connectionpool').setLevel(logging.INFO)
    logging.getLogger('gipc').setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    scheduler_thread = threading.Thread(target=start, args=())
    scheduler_thread.setDaemon(True)
    scheduler_thread.start()
    log.info(u'Scheduler Started.')
    srv = WSGIServer(('0.0.0.0', 5000),
                     app,
                     handler_class=WebSocketHandler,
                     log=log)
    log.info(u'Started Server.')
    srv.serve_forever()
    shutdown()
