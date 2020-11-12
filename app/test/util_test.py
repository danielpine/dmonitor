from app import util
from app.util.logger import log


def test_yaml():
    conf = util.load_yaml('config/app.yaml')
    log.info(conf)
