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
        config = dict([(key, value) for key, value in  self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in  config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:5000"
    }
    StandaloneApplication(app, options=options).run()
 
