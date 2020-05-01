# from languageProcessing import languageClassifier
import os
import plotly.graph_objects as go
import time
import shrimpy

from democlient import demowsclient
from arbitrage import currencymonitor

SHRIMPY_PUB_KEY = os.getenv('SHRIMPY_PUB_KEY')
SHRIMPY_PRV_KEY = os.getenv('SHRIMPY_PRV_KEY')
EXCH_PUB_KEY = os.getenv('EXCH_PUB_KEY')
EXCH_SEC_KEY = os.getenv('EXCH_SEC_KEY')

client = None
wsClient_btc_eth = None
wsClient_eth_zec = None
wsClient_zec_btc = None

def error_ws_handler(msg):
    print("webSocket error: ", msg)
    print("STOPPING Arbitrage Server")
    exit(1)


if SHRIMPY_PRV_KEY is not None and SHRIMPY_PUB_KEY is not None and EXCH_PUB_KEY is not None and EXCH_SEC_KEY is not None:
    client = shrimpy.ShrimpyApiClient(SHRIMPY_PUB_KEY, SHRIMPY_PRV_KEY)
    raw_token_B_E = client.get_token()
    raw_token_E_L = client.get_token()
    raw_token_L_B = client.get_token()
    wsClient_btc_eth = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_B_E['token'])
    wsClient_eth_zec = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_E_L['token'])
    wsClient_zec_btc = shrimpy.ShrimpyWsClient(error_ws_handler, raw_token_L_B['token'])
else:
    wsClient_btc_eth = demowsclient.DemoWSClient()
    wsClient_eth_zec = demowsclient.DemoWSClient()
    wsClient_zec_btc = demowsclient.DemoWSClient()

monitorBTC_ETH = currencymonitor.CurrencyMonitor('eth', 'btc', wsClient_btc_eth)
monitorETH_ZEC = currencymonitor.CurrencyMonitor('zec', 'eth', wsClient_eth_zec)
monitorZEC_BTC = currencymonitor.CurrencyMonitor('zec', 'btc', wsClient_zec_btc)

monitorBTC_ETH.start_monitor()
monitorETH_ZEC.start_monitor()
monitorZEC_BTC.start_monitor()

for n in range(0, 100):
    time.sleep(0.200)
    print("BTC_ETH: ", monitorBTC_ETH.runningPrice)
    print("ETH_ZEC: ", monitorETH_ZEC.runningPrice)
    print("ZEC_BTC: ", monitorZEC_BTC.runningPrice)

monitorBTC_ETH.stop_monitor()
monitorETH_ZEC.stop_monitor()
monitorZEC_BTC.stop_monitor()

# So long as I'm trading between cryptocurrencies, my fees are broken down as follows.
# I will not always be charged every fee. It depends on my load, market volatility, amount, and more.
# Nevertheless, this is the maximum percentage I can be charged for transactions below and equivalent 1,000,000 million USD.
# See: https://gemini.com/fees/api-fee-schedule#api-fee
fee = 0.00350 + 0.00100 + 0.00200 # Taker Fee + Maker Fee + Auction Fee = 0.0065 PER LIMIT TRADE


# Get our list of users.
users = client.list_users()
first_user_id = users[0]['id']

# Get the accounts for this user
accounts = client.list_accounts(
    first_user_id
)
first_account_id = accounts[0]['id']
#
# Get balance data for the user account you previously created
balance = client.get_balance(
    first_user_id,   # user_id
    first_account_id # account_id
)

print(balance)

# Make a market order
# def make_an_order(from_currency, to_currency, amount_from_currency):
#     smart_order_response = client.create_trade(
#         first_user_id,          # user_id
#         first_account_id,       # account_id
#         from_currency,          # Ex: 'BTC'
#         to_currency,            # Ex: 'ETH'
#         amount_from_currency,   # amount of from_currency
#         True                    # enable smart_routing
#     )
#
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






