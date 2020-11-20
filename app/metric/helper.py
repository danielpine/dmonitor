from app.util.timer import format_time
import time

import psutil
from app.util import get_mem_size, convert_json_from_lists
from app.util.logger import log


keys = ["timestamp", "pid", "pname", "mem", "cpu"]


def list_realtime_metrics(fmt=None):
    data = []
    tms = int(time.time())
    log.info('Reading process info... %s', tms)
    for p in psutil.process_iter():
        data.append((tms, p.pid, p.name(), get_mem_size(p),
                     float(format(p.cpu_percent(), '.2f'))))
    if fmt is None:
        return data
    elif fmt == 'json':
        return convert_json_from_lists(keys, data)


def quiet_exec(fun):
    try:
        result = fun()
        return result
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return ''


def list_process_detail_csv():
    data = []
    title = 'Pid,Ppid,Name,MemUsed,Cpu_Percent,Cmdline'
    data.append(title)
    for p in psutil.process_iter():
        data.append(','.join([str(e) for e in [p.pid, p.ppid(), p.name(), get_mem_size(
            p), p.cpu_percent(), '"'+' '.join(quiet_exec(p.cmdline))+'"']]))
    return '\n'.join(data)


if __name__ == '__main__':
    ps = list_process_detail_csv()
    print(ps)
