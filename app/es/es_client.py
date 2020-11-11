from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    cloud_id="memory-optimized-deployment:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJGFmODk4NzJhMzE0ODQ0Y2FhYTQ4MTNkY2VhNzVhNzIyJGJmZWE4MWQ2MjBkNjRlYmM5MjJmNTM2M2M2ZWZiODk0",
    http_auth=("elastic", "RG67D52RVbmSSshZwuIyFNSN"),
)


def load_es_conf():
    return json.load(open('app/conf/elasticsearch_index_template.json'))


def test_ex():
    conf = load_es_conf()
    result = es.indices.delete(index='record', ignore=[400, 404])
    # print(result)
    result = es.indices.create(index='record', body=conf, ignore=400)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_ex()
