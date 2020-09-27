from flask import request, Flask
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
log=logging.getLogger()
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


if __name__ == "__main__":
    logging.getLogger('PokeAlarm').setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.INFO)
    logging.getLogger('pyswgi').setLevel(logging.INFO)
    logging.getLogger('connectionpool').setLevel(logging.INFO)
    logging.getLogger('gipc').setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    log.info(u'Started.')
    srv = WSGIServer(('0.0.0.0', 5000), app,
                     handler_class=WebSocketHandler, log=log)
    d=os.popen('tasklist')
    log.info(d.read())
    srv.serve_forever()
