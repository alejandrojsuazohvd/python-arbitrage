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
import time
from decimal import *

# So long as I'm trading between cryptocurrencies, my fees are broken down as follows.
# I will not always be charged every fee. It depends on my load, market volatility, amount, and more.
# Nevertheless, this is the maximum percentage I can be charged for transactions below and equivalent 1,000,000 million USD.
# See: https://gemini.com/fees/api-fee-schedule#api-fee
fee = 0.00350 + 0.00100 + 0.00200  # Taker Fee + Maker Fee + Auction Fee = 0.0065 PER LIMIT TRADE


class Arbitrage:
    # Expects an API self.client and an array of currency monitors
    def __init__(self, client, currency_monitors):
        if client is None:
            print("API self.client is None for arbitrage")
            exit(2)

        self.client = client
        self.currency_monitors = currency_monitors
        self.user_id = ''
        self.account_id = ''
        self.balance = 0.0
        self.setup_account_information()
        self.workerThread = threading.Thread(target=self.do_arbitrage, args=())
        self.books = {}
        self.shouldArbitrage = False

    def setup_account_information(self):
        # Get our list of users.
        users = self.client.list_users()
        self.user_id = users[0]['id']

        # Get the exchange accounts for this user
        accounts = self.client.list_accounts(
            self.user_id
        )
        self.account_id = accounts[0]['id']

        self.get_balance_info()

    def get_balance_info(self):
        # Get balance data for user and exchange of that user
        self.balance = self.client.get_balance(
            self.user_id,
            self.account_id
        )

        return self.balance

    def get_value_from_balance(self, currency):
        # Balance will have contents like: {'retrievedAt': '2020-05-02T17:16:17.000Z', 'balances': [{'symbol': 'USD', 'nativeValue': 1, 'btcValue': 0.000111548758909942, 'usdValue': 1}, {'symbol': 'BTC', 'nativeValue': 0.00442322496144, 'btcValue': 0.00442322496144, 'usdValue': 39.6528388541828}, {'symbol': 'ETH', 'nativeValue': 0.041382, 'btcValue': 0.00098820216, 'usdValue': 8.8589256362576}]}
        for balance in self.balance['balances']:
            if balance['symbol'] == currency.upper():
                return balance['nativeValue']

        print("ERROR: No balance found for symbol: ", currency)
        return '0'

    # Log to a file by appending.
    def log(self, content):
        f = open("trade-log.txt", "a")
        f.write(str(content))
        f.close()

    # Need to make sure that the log is non blocking so trades can continue.
    def non_blocking_log(self, content):
        logThread = threading.Thread(target=self.log, args=(content,))
        logThread.start()

    # Make a market order/trade (limit order)
    def make_an_order(self, from_currency, to_currency, amount_from_currency):
        order_response = self.client.create_trade(
            self.user_id,          # user_id
            self.account_id,       # account_id
            from_currency,          # Ex: 'BTC'
            to_currency,            # Ex: 'ETH'
            amount_from_currency,   # amount of from_currency
            True                    # enable Shrimpy smart_routing
        )

        logDict = {'msg': 'Order made!', 'from': from_currency, 'to': to_currency, 'amount': amount_from_currency, 'tradeMeta': order_response}
        self.non_blocking_log(logDict
                              )
        return order_response

    # Book data will use Decimal to represent monetary value since Floats and doubles have dubious precision.
    def populate_book_data(self):
        for monitor in self.currency_monitors:
            if monitor.runningPrice.get('content') is None:
                # We exit method if any piece of information is missing
                return False

            bookName = monitor.from_currency + '-' + monitor.to_currency
            inverseBookName = monitor.to_currency + '-' + monitor.from_currency
            self.books[bookName] = Decimal(monitor.runningPrice['content']['asks'][0]['price'])  # Going with the ask instead of bid to avoid shortchanges.
            # Potentially risky below.
            self.books[inverseBookName] = Decimal(1.0) / Decimal(monitor.runningPrice['content']['asks'][0]['price']) # Due to the unavailability of inverse trades books on Gemini, I will use the inverse of the original book

        return True

    # This is crux of all of the work on this project. This handles the running state of a triangular arbitrage.
    #           ... -> A <-> B <-> C <- ...
    # The algorithm is as follows,
    # We have prices of trade pairs
    #  if AB, BC, CA, BA, CB, and AC
    #          then if the ratio of price between AB is ratio_1, AC is ratio_2, CB is ratio_3
    #               if ratio_1 > ratio_2 & ratio_3
    #                    then trade A -> C -> B -> A
    # Ex: If the ratios are as follows
    #    2:4 > 1:2 & 2:3
    #       then A -> C -> B -> A would have a 50% return on investment.
    # Then we continue to do this comparison. BTC is the most truthful orderbook so we will keep our running balance on BTC
    # 2nd problem: trade fees.
    # So I determined the maximum fees per trade and the GAIN after the trade has COVER the fee costs.
    # so this now requires the algorithm to determine potential gain on prior to committing a transaction
    # The condition is as follows
    # if ratio_AB > ratio_AC & ratio_CB
    #   AND ratio_AC & ratio_CB & ratio_BA > fee %
    #     then trade A -> C -> B -> A
    def analyze_book_data(self, pair1, pair2, pair3):
        # I leverage the prices defined here due to the prices always being valued to the amount of from_currency to ONE to_currency
        ratio_1 = self.books[pair1]  # Ex: 'btc-eth'
        ratio_2 = self.books[pair2]  # Ex: 'btc-zec'
        ratio_3 = self.books[pair3]  # Ex: 'zec-eth'
        ratio_2_3 = ratio_2 * ratio_3
        if ratio_1 > ratio_2_3 and ratio_1 / ratio_2_3 > fee * 3:
            return True
        else:
            return False

    def get_active_trades(self):
        return self.client.list_active_trades(
            self.user_id,  # user_id
            self.account_id,  # account_id
        )

    def make_arbitrage_orders(self, orderedTradesArrays):
        for trade in orderedTradesArrays:
            # Wait for any previous trades to complete. get_active_trades returns an empty array when there are only trades with 'completed' status
            while self.get_active_trades(): # Due to python booleaness this evaluates to true if not empty and false if empty
                time.sleep(0.100)

            self.get_balance_info()  # Get running balance to know how much to trade.
            self.make_an_order(trade['from_currency'],
                               trade['to_currency'],
                               self.get_value_from_balance(trade['from_currency']))

    # For timely's sake I will only support two trade routes BTC -> ETH -> ZEC -> BTC and BTC -> ZEC -> ETH -> BTC
    def do_arbitrage(self):
        while self.shouldArbitrage:
            if not self.populate_book_data():
                continue  # Short circuit and do NOT trade if the book data has not completely been populated.

            should_trade = self.analyze_book_data('btc-eth', 'btc-zec', 'zec-eth')
            if should_trade:
                self.make_arbitrage_orders([{'from_currency': 'btc', 'to_currency': 'zec'},
                                            {'from_currency': 'zec', 'to_currency': 'eth'},
                                            {'from_currency': 'eth', 'to_currency': 'btc'}])

            should_trade = self.analyze_book_data('btc-zec', 'btc-eth', 'eth-zec')
            if should_trade:
                self.make_arbitrage_orders([{'from_currency': 'btc', 'to_currency': 'eth'},
                                            {'from_currency': 'eth', 'to_currency': 'zec'},
                                            {'from_currency': 'zec', 'to_currency': 'btc'}])

    def begin_arbitrage(self):
        for monitor in self.currency_monitors:
            monitor.start_monitor()

        self.shouldArbitrage = True
        self.workerThread.start()

    def end_arbitrage(self):
        self.shouldArbitrage = False
        self.workerThread.join()
        for monitor in self.currency_monitors:
            monitor.stop_monitor()