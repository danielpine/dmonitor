from app import util
from app.util.logger import log


def test_yaml():
    conf = util.load_yaml('config/application.yml')
    log.info(conf)

def test_json():
    conf= util.load_json('config/elasticsearch_index_system.json')
    print(conf['force'])


test_json()