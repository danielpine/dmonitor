from app.es import client
from app.metric.abstract_data_processor import AbstractDataProcessor
from app.util.logger import log
import re


def fill_wildcard(keyword):
    return '%'+'%'.join(re.sub('[\s+]', '', keyword))+'%'


class ElasticSearchDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query(start, end, wildcard):
        return client.excute_sql("select * from record where pname like '%s' and timestamp between '%s' and '%s' order by timestamp" % (wildcard, start, end))

    @staticmethod
    def query_process_by_key_words(parm):
        wildcard = fill_wildcard(parm.get('key_words'))
        start = parm.get('start')
        end = parm.get('end')
        log.warn(wildcard + start + end)
        return client.excute_sql("select pname from record where pname like '%s' and timestamp between '%s' and '%s' group by pname" % (wildcard, start, end))
