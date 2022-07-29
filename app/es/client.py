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
es = Elasticsearch("http://%s:%s" % (APP_SETTINGS.prop('dmonitor.es.host'),APP_SETTINGS.prop('dmonitor.es.port')))

def exists(index):
    return es.indices.exists(index=index, ignore=[400, 404])


def create(index, body=None, force=None):
    """
    创建索引
    :param index: 索引名称
    :return: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'student1'}
    """
    if force:
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


def init_index_from_conf(path):
    conf = util.load_json(path)
    res = create(conf['index'], body=conf['body'], force=conf['force'])
    log.warn(res)


def init():
    init_index_from_conf('config/elasticsearch_index_record.json')
    init_index_from_conf('config/elasticsearch_index_system.json')


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
    log.warn(sql)
    query = {
        "query": sql,
        "fetch_size": 10000
    }
    return re.sub('\r', '', es.sql.query(query, format=format))


if __name__ == "__main__":
    # r = excute_sql(r"select count(*) from record where pname like 'rcuos/1%' ")
    # r = excute_sql(
    # r"SELECT pname FROM record WHERE pname like '%Code%'  GROUP BY pname")
    init()
