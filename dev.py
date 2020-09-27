from flask import request, Flask
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
import logging

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
user_socket_list = []
log=logging.getLogger("logger")

@app.route('/orange')
def orange():
    user_socket = request.environ.get('wsgi.websocket')
    print('request', request)
    print('user_socket', user_socket)
    if user_socket:
        user_socket_list.append(user_socket)
        print('user_socket_list depth', len(user_socket_list))
    while True:
        msg = user_socket.receive()
        print('received:', msg)
        for sock in user_socket_list:
            try:
                sock.send('received:' + msg)
            except:
                continue


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    log.setLevel(logging.INFO)
    logging.getLogger('PokeAlarm').setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('pyswgi').setLevel(logging.WARNING)
    logging.getLogger('connectionpool').setLevel(logging.WARNING)
    logging.getLogger('gipc').setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    log.info('Started.')
    srv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler,log=logging.getLogger('pyswgi'))
    srv.serve_forever()