# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Pine
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from app.metric.database_data_processor import DataBaseDataProcessor
from app.metric.elasticsearch_data_processor import ElasticSearchDataProcessor

from config import APP_SETTINGS


def get_data_processor():
    store = APP_SETTINGS.prop('dmonitor.store')
    if store == 'ES':
        return ElasticSearchDataProcessor
    elif store == 'DB':
        return DataBaseDataProcessor
    else:
        raise Exception('Not support storeage type.')


class DataProcessor(get_data_processor()):
    pass
