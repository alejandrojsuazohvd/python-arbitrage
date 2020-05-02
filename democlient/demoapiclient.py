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

import time
import threading
import uuid

# This client emulates the shrimpy python API client for testing and demonstration purposes.
# To demonstrate proper trading mechanisms and avoid real trades on my personal finances.
class DemoAPIClient:

    def __init__(self):
        # Formatted like shrimpy API: https://developers.shrimpy.io/docs/#balances
        self.balance = {'retrievedAt': '2020-05-02T17:16:17.000Z', 'balances': [{'symbol': 'BTC', 'nativeValue': 1, 'btcValue': 1, 'usdValue': 1}]}
        self.active_trades = []

    def list_users(self):
        return [{'id': '1'}]

    def list_accounts(self, user_id):
        return [{'id': '012'}]

    def get_balance(self, user_id, account_id):
        return self.balance

    def add_active_trade(self, from_currency, to_currency, amount):
        # Will add an active trade formatted like the real API https://developers.shrimpy.io/docs/#list-active-trades
        # Using a UUID.
        self.active_trades.append({
                "id": uuid.uuid4(),
                "fromSymbol": from_currency,
                "toSymbol": to_currency,
                "amount": amount,
                "status": "queued",
                "success": False,
                "errorCode": 0,
                "errorMessage": "",
                "exchangeApiErrors": [],
                "smartRouting": False,
                "maxSpreadPercent": "10",
                "maxSlippagePercent": "10",
                "triggeredMaxSpread": False,
                "triggeredMaxSlippage": False
            })

        time.sleep(2.0)  # This will Rate limit the demonstration trades to a manageable frequency to show proper logs.
        self.active_trades = []

    def make_timed_active_trade(self, from_currency, to_currency, amount_from_currency):
        activeTradeThread = threading.Thread(target=self.add_active_trade, args=(from_currency, to_currency, amount_from_currency,))
        activeTradeThread.start()

    def create_trade(self, user_id, account_id, from_currency, to_currency, amount_from_currency, smart_route):
        # Emulate a balance change
        self.balance['balances'][0]['symbol'] = to_currency.upper()
        self.make_timed_active_trade(from_currency, to_currency, amount_from_currency)
        return {'id': 'Demonstration trade NO REAL MONEY HAS BEEN EXCHANGED. ', }


    def list_active_trades(self, user_id, account_id):
        return self.active_trades

