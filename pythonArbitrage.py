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
import shrimpy
import http.server
import socketserver
import os.path

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

if not os.path.exists("index.html"):
    with open("index.html", "w") as f:
        f.write("<h2>Alejandro's Arbitrage Trading Logs</h2>")

PORT = 8081

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()







