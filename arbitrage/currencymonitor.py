import threading


class CurrencyMonitor:

    def __init__(self, from_currency, to_currency, client):
        self.currencyPair = from_currency + "-" + to_currency
        self.runningPrice = {}
        self.client = client
        self.workerThread = threading.Thread(target=self.run_socket_connection_for_crypto_pair, args=())

    def handler(self, msg):
        # Expected msg format:
        # {'exchange': 'gemini', 'pair': 'ltc-eth', 'channel': 'orderbook', 'snapshot': False, 'sequence': 3521409, 'content': {'asks': [{'price': '0.2245', 'quantity': '1'}], 'bids': []}}
        self.runningPrice = msg

    def run_socket_connection_for_crypto_pair(self):
        # chart_exchange_rate_for_transaction('eth', 'btc')
        subscribe_data = {
            "type": "subscribe",
            "exchange": "gemini",
            "pair": self.currencyPair,
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
        self.workerThread.join()
        self.client.disconnect()
