import json
from app import util
import re
DEFAULT_CONFIG_PATH = 'config/app.yaml'


class Configuration(object):

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.globel_app_conf = util.load_yaml(path)

    def prop(self, want):
        wants = re.split('\.', want, 1)
        end = self.globel_app_conf
        for key in wants:
            end = end[key]
        return end


APP_SETTINGS = Configuration()

print(APP_SETTINGS.globel_app_conf)
print(APP_SETTINGS.prop('dmonitor.store'))
