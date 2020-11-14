

from app.metric import DataProcessor


def test_data_processor():
    DataProcessor.query()
    print(DataProcessor.query_monprocess())


test_data_processor()
