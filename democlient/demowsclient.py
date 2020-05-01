import random
import time


# This demo client emulates the same interface that the shrimpy-pythyon web socket client does to facilitate demonstration of
# functionality.
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
                    'content': {'asks': [{'price': random.uniform(0.0, 2.0)}], 'bids': [{}]}}
        return dataDict

    def subscribe(self, config, handler):
        self.subscriptionRunning = True
        while self.subscriptionRunning:
            time.sleep(1)
            handler(self.generate_data(config))

    def disconnect(self):
        self.subscriptionRunning = False