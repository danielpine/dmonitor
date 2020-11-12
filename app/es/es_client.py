from elasticsearch import Elasticsearch
from app import util

es = Elasticsearch(
    cloud_id="memory-optimized-deployment:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJGFmODk4NzJhMzE0ODQ0Y2FhYTQ4MTNkY2VhNzVhNzIyJGJmZWE4MWQ2MjBkNjRlYmM5MjJmNTM2M2M2ZWZiODk0",
    http_auth=("elastic", "RG67D52RVbmSSshZwuIyFNSN"),
)


def test_ex():
    conf = util.load_json('config/elasticsearch_index_record.json')
    print(conf)


if __name__ == "__main__":
    test_ex()
