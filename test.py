import psutil

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
log=logging.getLogger()

def get_mem_size(process):
    mem_info = process.memory_info()
    return mem_info.rss / 1024

data=[]

log.info('start')
for p in psutil.process_iter():
    # log.info("pid : %s pname: %s mem: %10f kb" ,p.pid, p.name(), get_mem_size(p))
    data.append((p.pid, p.name(), get_mem_size(p)))
log.info('done')
for m in data:
    log.info("pid : %s pname: %s mem: %10f kb" ,m[0],m[1],m[2])
