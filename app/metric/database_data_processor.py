from app.data import (select_from_record, select_from_record_filter,
                      select_process_from_record_by_key_words)
from app.metric.abstract_data_processor import AbstractDataProcessor
from app.util.logger import log

title = ['timestamp', 'pid', 'pname', 'mem', 'cpu']


class DataBaseDataProcessor(AbstractDataProcessor):
    @staticmethod
    def query(start, end, wildcard):
        records = []
        if wildcard and len(wildcard.strip()) > 0:
            records = select_from_record_filter(start, end, wildcard)
        else:
            records = select_from_record(start, end)
        lines = [','.join(title)]
        for row in records:
            
            lines.append(','.join([str(i) for i in row]))
        return '\n'.join(lines)

    @staticmethod
    def query_process_by_key_words(parm):
        key_words = parm.get('key_words')
        log.warn(key_words)
        data = select_process_from_record_by_key_words('%'+key_words+'%')
        data.insert(0, 'pname')
        return '\n'.join(data)
