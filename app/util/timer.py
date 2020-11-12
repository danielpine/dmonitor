import time

from app.util.logger import log

DEFAULT_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"


def format_time(timestamp, fmt=DEFAULT_TIME_FORMAT):
    return time.strftime(fmt, time.localtime(timestamp))


class Timer(object):
    def __init__(self):
        self._start = 0
        self._is_start = False
        pass

    def start(self):
        self._is_start = True
        self._start = time.time()

    def reset(self):
        self._start = time.time()

    def duration(self, note=''):
        now = time.time()
        ela = now - self._start
        log.warn("%s timer(%s) from %s to %s , elapsed time %.4f s", note, id(self),
                 format_time(self._start), format_time(now), ela)
        return ela
