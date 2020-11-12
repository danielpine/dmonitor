from app.util.timer import Timer
from app.util.logger import log
from app import util
from app.util import metric_helper
from config import APP_SETTINGS
from elasticsearch import Elasticsearch, helpers

# 链接es服务
es = Elasticsearch(APP_SETTINGS.prop('dmonitor.es.host'),
                   port=APP_SETTINGS.prop('dmonitor.es.port'))


def exists(index):
    return es.indices.exists(index=index, ignore=[400, 404])


def create(index, body=None):
    """
    创建索引
    :param index: 索引名称
    :return: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'student1'}
    """
    delete(index)
    return es.indices.create(index=index, body=body, ignore=400)


def delete(index):
    """
    删除索引
    :param index: 索引名称
    :return: True 或 False
    """
    if exists(index):
        return es.indices.delete(index=index, ignore=[400, 404])['acknowledged']
    else:
        return False


def index(index, body, id=None):
    return es.index(index=index, body=body, id=id)['_id']


def search(index=None):
    if index:
        return es.search(index=index)
    else:
        return es.search()


def main():
    import uuid
    conf = util.load_json('config/elasticsearch_index_record.json')
    res = create(conf['index'], body=conf['body'])
    log.info(res)
    timer = Timer()
    process_info_list = metric_helper.list_realtime_metrics(fmt='json')
    timer.start()
    for action in process_info_list:
        es.index(index='record', body=action)
    timer.duration('fore')
    process_info_list = metric_helper.list_realtime_metrics(fmt='json')
    timer.reset()
    actions = [
        {
            "_index": 'record',
            "_id":  uuid.uuid1().hex.upper(),
            "_source": action
        } for action in process_info_list
    ]
    res = helpers.bulk(es, actions)
    timer.duration('bulk')
    log.info(res)


if __name__ == '__main__':
    main()
