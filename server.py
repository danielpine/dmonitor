from flask import Flask
app = Flask(__name__,static_url_path='')
 
@app.route('/')
def hello_world():
    return app.send_static_file('index.html')
 
import gunicorn.app.base


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """
    Custom application
    """

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        "bind": "127.0.0.1:8000"
    }
    StandaloneApplication(app, options=options).run()
 