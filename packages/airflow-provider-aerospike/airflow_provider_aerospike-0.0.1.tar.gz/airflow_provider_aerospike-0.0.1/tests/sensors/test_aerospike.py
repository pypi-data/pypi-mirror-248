#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import unittest
from unittest.mock import patch, Mock
from aerospike_provider.sensors.aerospike import AerospikeKeySensor
import aerospike

class TestAerospikeKeySensor(unittest.TestCase):
    def setUp(self):
        self.namespace = 'test_namespace'
        self.set = 'test_set'
        self.key = 'test_key'
        self.policy = { aerospike.POLICY_KEY_SEND }
        self.task_id = 'test_task'
        self.metadata = {'ttl': 1000, 'gen': 4}
        self.bins = {'name': 'Aerospike Test', 'version': "1.0.0"}

        self.sensor = AerospikeKeySensor(
            namespace=self.namespace,
            set=self.set,
            key=self.key,
            policy=self.policy,
            task_id=self.task_id
        )

    @patch('aerospike_provider.hooks.aerospike.AerospikeHook.get_conn')
    def test_poke(self, mock_hock_conn):
        mock_hock_conn.return_value = Mock()
        self.sensor.parse_records = Mock()
        self.sensor.parse_records.return_value = [1]
        self.sensor.poke({})

        mock_hock_conn.return_value.exists.assert_called_once_with(
            namespace='test_namespace',
            set='test_set',
            key='test_key',
            policy={ aerospike.POLICY_KEY_SEND }
        )

    def test_parse_records_with_existing_key_as_tuple(self):
        mock = ( (self.namespace, self.set, self.key), self.metadata, self.bins)
        mock_parsed = self.sensor.parse_records(records=mock)
        expected = True
        assert mock_parsed == expected

    def test_parse_records_with_no_existing_key_as_tuple(self):
        mock = ( (self.namespace, self.set), None)              # Expecting None instead of metadata when key not exists.
        mock_parsed = self.sensor.parse_records(records=mock)
        expected = False
        assert mock_parsed == expected


    def test_parse_records_existing_keys_as_list(self):
        mock = [( (self.namespace, self.set, self.key), self.metadata, self.bins), ( (self.namespace, self.set, self.key), self.metadata, self.bins)]
        mock_parsed = self.sensor.parse_records(records=mock)
        expected = True
        assert mock_parsed == expected


    def test_parse_records_no_existing_keys_as_list(self):
        mock = [
            ( (self.namespace, self.set, 'non existing key'), None),  # Expecting None instead of metadata when key not exists.
            ( (self.namespace, self.set, self.key), self.metadata, self.bins)
        ]
        mock_parsed = self.sensor.parse_records(records=mock)
        expected = False
        assert mock_parsed == expected

    def test_parse_records_as_exception(self):
        mock = {}
        with self.assertRaises(ValueError):
            self.sensor.parse_records(records=mock)
