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

import abc
import socket
import time
from app.data import MonProcessState, insert_many_to_monprocess, select_all_monprocess


class AbstractDataProcessor(metaclass=abc.ABCMeta):
    """ Abstract Data Processor for handling data query. """
    @abc.abstractstaticmethod
    def query():
        """query metric data set"""
        raise NotImplementedError("Not Implemented Method query()")

    @staticmethod
    def query_monprocess():
        return select_all_monprocess()

    @staticmethod
    def insert_monprocess(parm):
        hostname = socket.gethostname()
        insert_many_to_monprocess(
            [(hostname, MonProcessState.ON.value, parm.get('key'), parm.get('type'), int(time.time()))])
        return {'code': 1, 'msg': ''}
