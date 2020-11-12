from app import util


def test_yaml():
    conf = util.load_yaml('config/app.yaml')
    print(conf)


test_yaml()
