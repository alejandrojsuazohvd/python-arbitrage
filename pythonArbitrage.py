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

# from languageProcessing import languageClassifier
import os
import plotly.graph_objects as go
import time
import shrimpy

from arbitrage.arbitrage import Arbitrage
from democlient import demowsclient
from arbitrage import currencymonitor
from democlient.demoapiclient import DemoAPIClient

SHRIMPY_PUB_KEY = os.getenv('SHRIMPY_PUB_KEY')
SHRIMPY_PRV_KEY = os.getenv('SHRIMPY_PRV_KEY')
EXCH_PUB_KEY = os.getenv('EXCH_PUB_KEY')
EXCH_SEC_KEY = os.getenv('EXCH_SEC_KEY')

client = None
wsClient_btc_eth = None
wsClient_zec_eth = None
wsClient_zec_btc = None

def error_ws_handler(msg):
    print("webSocket error: ", msg)
    print("STOPPING Arbitrage Server")
    exit(1)


if SHRIMPY_PRV_KEY is not None and SHRIMPY_PUB_KEY is not None and EXCH_PUB_KEY is not None and EXCH_SEC_KEY is not None:
    client = shrimpy.ShrimpyApiClient(SHRIMPY_PUB_KEY, SHRIMPY_PRV_KEY)
    raw_token_B_E = client.get_token()
    raw_token_Z_E = client.get_token()
    raw_token_Z_B = client.get_token()
    wsClient_btc_eth = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_B_E['token'])
    wsClient_zec_eth = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_Z_E['token'])
    wsClient_zec_btc = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_Z_B['token'])
else:
    client = DemoAPIClient()
    wsClient_btc_eth = demowsclient.DemoWSClient()
    wsClient_zec_eth = demowsclient.DemoWSClient()
    wsClient_zec_btc = demowsclient.DemoWSClient()

monitorBTC_ETH = currencymonitor.CurrencyMonitor('eth', 'btc', wsClient_btc_eth)
monitorZEC_ETH = currencymonitor.CurrencyMonitor('zec', 'eth', wsClient_zec_eth)
monitorZEC_BTC = currencymonitor.CurrencyMonitor('zec', 'btc', wsClient_zec_btc)

arbitrage = Arbitrage(client, [monitorBTC_ETH, monitorZEC_ETH, monitorZEC_BTC])

arbitrage.begin_arbitrage()

# print(arbitrage.make_an_order('ETH', 'BTC', 0.041382))
# print(arbitrage.get_active_trades())


# monitorBTC_ETH.start_monitor()
# monitorETH_ZEC.start_monitor()
# monitorZEC_BTC.start_monitor()
#
# for n in range(0, 100):
#     time.sleep(0.200)
#     print("BTC_ETH: ", monitorBTC_ETH.runningPrice)
#     print("ETH_ZEC: ", monitorETH_ZEC.runningPrice)
#     print("ZEC_BTC: ", monitorZEC_BTC.runningPrice)
#
# monitorBTC_ETH.stop_monitor()
# monitorETH_ZEC.stop_monitor()
# monitorZEC_BTC.stop_monitor()


# def chart_exchange_rate_for_transaction(from_currency, to_currency):
#     candles = client.get_candles(
#         'bittrex', # exchange
#         from_currency,     # base_trading_symbol
#         to_currency,     # quote_trading_symbol
#         '1d'       # interval
#     )
#
#     dates = []
#     open_data = []
#     high_data = []
#     low_data = []
#     close_data = []
#
#     # format the data to match the plotting library
#     for candle in candles:
#         dates.append(candle['time'])
#         open_data.append(candle['open'])
#         high_data.append(candle['high'])
#         low_data.append(candle['low'])
#         close_data.append(candle['close'])
#
#     # plot the candlesticks
#     fig = go.Figure(data=[go.Candlestick(x=dates,
#                            open=open_data, high=high_data,
#                            low=low_data, close=close_data)])
#     fig.show()






