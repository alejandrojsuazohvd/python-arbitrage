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
import threading


class CurrencyMonitor:

    def __init__(self, from_currency, to_currency, client):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.runningPrice = {}
        self.client = client
        self.workerThread = threading.Thread(target=self.run_socket_connection_for_crypto_pair, args=())

    def handler(self, msg):
        # Expected msg format:
        # {'exchange': 'gemini', 'pair': 'zec-eth', 'channel': 'orderbook', 'snapshot': False, 'sequence': 3521409, 'content': {'asks': [{'price': '0.2245', 'quantity': '1'}], 'bids': []}}
        self.runningPrice = msg

    def run_socket_connection_for_crypto_pair(self):
        # chart_exchange_rate_for_transaction('eth', 'btc')
        subscribe_data = {
            "type": "subscribe",
            "exchange": "gemini",
            "pair": self.from_currency + "-" + self.to_currency,
            "channel": "orderbook"
        }

        # Start processing the websocket stream!
        self.client.connect()
        self.client.subscribe(subscribe_data, self.handler)

    def start_monitor(self):
        if self.client is None:
            print("Error, no valid client provided")
        self.workerThread.start()

    def stop_monitor(self):
        self.client.disconnect()
        self.workerThread.join()
