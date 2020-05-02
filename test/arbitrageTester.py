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

import unittest

from arbitrage.arbitrage import Arbitrage
from arbitrage.currencymonitor import CurrencyMonitor
from democlient.demoapiclient import DemoAPIClient


class TestArbitrage(unittest.TestCase):

    currencyMonitor1 = CurrencyMonitor('btc', 'eth', None)
    currencyMonitor2 = CurrencyMonitor('btc', 'zec', None)
    currencyMonitor3 = CurrencyMonitor('zec', 'eth', None)
    arbitrage = Arbitrage(DemoAPIClient(), [currencyMonitor1, currencyMonitor2, currencyMonitor3])

    def test_arbitrage_analyzer_ShouldTrade(self):
        self.currencyMonitor1.runningPrice = {'exchange': 'gemini', 'pair': 'btc-eth', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '6', 'quantity': '1'}], 'bids': []}}
        self.currencyMonitor2.runningPrice = {'exchange': 'gemini', 'pair': 'btc-zec', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '2', 'quantity': '1'}], 'bids': []}}
        self.currencyMonitor3.runningPrice = {'exchange': 'gemini', 'pair': 'zec-eth', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '2', 'quantity': '1'}], 'bids': []}}

        self.arbitrage.populate_book_data()
        self.assertTrue(self.arbitrage.analyze_book_data('btc-eth', 'btc-zec', 'zec-eth'))

    def test_arbitrage_analyzer_ShouldNOTTrade(self):
        self.currencyMonitor1.runningPrice = {'exchange': 'gemini', 'pair': 'btc-eth', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '3', 'quantity': '1'}], 'bids': []}}
        self.currencyMonitor2.runningPrice = {'exchange': 'gemini', 'pair': 'btc-zec', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '2', 'quantity': '1'}], 'bids': []}}
        self.currencyMonitor3.runningPrice = {'exchange': 'gemini', 'pair': 'zec-eth', 'channel': 'orderbook',
                                              'snapshot': False, 'sequence': 3521409,
                                              'content': {'asks': [{'price': '2', 'quantity': '1'}], 'bids': []}}

        self.arbitrage.populate_book_data()
        self.assertFalse(self.arbitrage.analyze_book_data('btc-eth', 'btc-zec', 'zec-eth'))
