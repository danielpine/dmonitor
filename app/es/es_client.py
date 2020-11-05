from elasticsearch import Elasticsearch

es = Elasticsearch(
    cloud_id="memory-optimized-deployment:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJGFmODk4NzJhMzE0ODQ0Y2FhYTQ4MTNkY2VhNzVhNzIyJGJmZWE4MWQ2MjBkNjRlYmM5MjJmNTM2M2M2ZWZiODk0",
    http_auth=("elastic", "RG67D52RVbmSSshZwuIyFNSN"),
)

result = es.indices.create(index='record', ignore=400)
print(result)
result = es.indices.delete(index='record', ignore=[400, 404])
print(result)
