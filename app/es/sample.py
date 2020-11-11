from app.util.metric_helper import list_realtime_metrics
from elasticsearch import Elasticsearch


# 链接es服务
es = Elasticsearch(['192.168.142.129'], port=80)

# 索引名称
index_name = 'record'

# 指定mappings和settings
request_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "index.query.default_field": "timestamp",
        "index.mapping.ignore_malformed": "false",
        "index.mapping.coerce": "false",
        "index.query.parse.allow_unmapped_fields": "false"
    },
    "mappings": {
        "_source": {
            "enabled": "false"
        },
        "properties": {
            "timestamp": {
                "type": "date",
                "index": "false",
                "store": "false",
                "doc_values": "true"
            },
            "pname": {
                "type": "keyword",
                "index": "false",
                "store": "false",
                "doc_values": "true"
            },
            "pid": {
                "type": "integer",
                "index": "false",
                "store": "false",
                "doc_values": "true"
            },
            "mem": {
                "type": "integer",
                "index": "false",
                "store": "false",
                "doc_values": "true"
            },
            "cpu": {
                "type": "float",
                "index": "false",
                "store": "false",
                "doc_values": "true"
            }
        }
    }
}


def create(index, body=None):
    """
    创建索引
    :param index: 索引名称
    :return: {'acknowledged': True, 'shards_acknowledged': True, 'index': 'student1'}
    """
    if es.indices.exists(index=index, ignore=[400, 404]):
        es.indices.delete(index=index, ignore=[400, 404])  # 删除索引
    res = es.indices.create(index=index, body=body, ignore=400)
    return res


res = create(index_name, body=request_body)

print(res)


def delete(index):
    """
    删除索引
    :param index: 索引名称
    :return: True 或 False
    """
    if not es.indices.exists(index):
        return False
    else:
        res = es.indices.delete(index=index)
        return res['acknowledged']


def add(index, body, id=None):
    """
    (单条数据添加或更新)添加或更新文档记录，更新文档时传对应的id即可
    使用方法：
    `
    body = {"name": "long", "age": 11,"height": 111}
    add(index=index_name,body=body)
    或
    body = {"name": "long", "age": 11,"height": 111}
    add(index=index_name,body=body,id=1)
    `
    :param index: 索引名称
    :param body:文档内容
    :param id: 是否指定id,如不指定就会使用生成的字符串
    :return:{'_index': 'student1', '_type': '_doc', '_id': 'nuwKDXIBujABphC4rbcq', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}
    """
    res = es.index(index=index, body=body, id=id)
    return res['_id']  # 返回 id


def search(index=None):
    """
    查询记录：如果没有索引名称的话默认就会查询全部的索引信息
    :param index:查询的索引名称
    :return:
    """
    if not index:
        return es.search()
    else:
        return es.search(index=index)


def main():
    process_info_list = list_realtime_metrics()
    print(process_info_list)


if __name__ == '__main__':
    main()
