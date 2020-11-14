import re
import uuid
from sqlite3.dbapi2 import paramstyle

from app import util
from app.metric.helper import list_realtime_metrics
from app.util.logger import log
from app.util.timer import Timer
from config import APP_SETTINGS
from elasticsearch import Elasticsearch, helpers
from elasticsearch.compat import string_types
from elasticsearch.exceptions import SerializationError
from elasticsearch.serializer import DEFAULT_SERIALIZERS


class CSVSerializer(object):
    mimetype = "text/csv"

    def loads(self, s):
        return s

    def dumps(self, data):
        if isinstance(data, string_types):
            return data
        raise SerializationError("Cannot serialize %r into csv." % data)


# Extend the serializer to support CSV
DEFAULT_SERIALIZERS[CSVSerializer.mimetype] = CSVSerializer()
# link es service
es = Elasticsearch(APP_SETTINGS.prop('dmonitor.es.host'),
                   port=APP_SETTINGS.prop('dmonitor.es.port'))


def exists(index):
    return es.indices.exists(index=index, ignore=[400, 404])


def create(index, body=None, force="false"):
    """
    创建索引
    :param index: 索引名称
    :return: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'student1'}
    """
    if force == 'true':
        delete(index)
    elif exists(index):
        return {'info': 'index exists ignore by not set force.'}
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


def init():
    conf = util.load_json('config/elasticsearch_index_record.json')
    res = create(conf['index'], body=conf['body'],
                 force=APP_SETTINGS.prop('dmonitor.es.forcecreateindex'))
    log.info(res)


def write():
    timer = Timer()
    process_info_list = list_realtime_metrics(fmt='json')
    timer.start()
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


def excute_sql(sql, format='csv'):
    query = {
        "query": sql,
        "fetch_size": 10000,
        "from":26000
    }
    return re.sub('\r', '', es.sql.query(query, format=format))


if __name__ == "__main__":
    r = excute_sql(r"select count(*) from record where pname like 'rcuos/1%' ")
    print(r.split('\n'))
    print(len(r.split('\n')))
