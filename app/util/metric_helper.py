import time

import app.util
import psutil
from app.util.logger import log


def get_mem_size(process):
    mem_info = process.memory_info()
    return mem_info.rss / 1024


def list_realtime_metrics(fmt=None):
    data = []
    tms = int(time.time())*1000
    log.info(tms)
    for p in psutil.process_iter():
        data.append((tms, p.pid, p.name(), get_mem_size(p), p.cpu_percent()))
    if fmt is None:
        return data
    elif fmt == 'json':
        keys = ["timestamp", "pid", "pname", "mem", "cpu"]
        return app.util.convert_json_from_lists(keys, data)


if __name__ == '__main__':
    import json
    ps = list_realtime_metrics(fmt='json')
    print(json.dumps(ps, indent=2))
    with open('test.json', 'w') as f:
        f.write(json.dumps(ps, indent=2))
