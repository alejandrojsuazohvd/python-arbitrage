# Copyright 2020 Alejandro Suazo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import time


# This demo client emulates the same interface that the shrimpy-pythyon web socket client does to facilitate
# demonstration of functionality.
class DemoWSClient:

    def __init__(self):
        self.subscriptionRunning = False
        return

    def generate_data(self, config):
        dataDict = {'exchange': config['exchange'],
                    'pair': config['pair'],
                    'channel': 'orderbook',
                    'snapshot': False,
                    'sequence': random.randrange(1000000, 9999999),
                    'content': {'asks': [{'price': random.uniform(0.0, 0.70)}], 'bids': [{}]}}
        return dataDict

    def subscribe(self, config, handler):
        self.subscriptionRunning = True
        while self.subscriptionRunning:
            time.sleep(1)
            handler(self.generate_data(config))

    def connect(self):
        print("Demonstration client in use.")

    def disconnect(self):
        self.subscriptionRunning = False