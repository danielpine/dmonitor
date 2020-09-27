 from flask import Flask
app = Flask(__name__, static_folder='webApp', static_url_path='', instance_relative_config=True)
socketio = SocketIO(app, async_mode='gevent')

 
@app.route('/')
def hello_world():
    return app.send_static_file('index.html')
 
if __name__ == '__main__':
    socketio.run(app)