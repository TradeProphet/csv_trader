import logging, os, datetime
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import sys
import pandas as pd


logging.getLogger("urllib3").setLevel(logging.WARNING)


class AlpacaLiveBroker:
    def __init__(self, key_id, secret_key, verbose=True, base_url = 'https://paper-api.alpaca.markets'):
        self.verbose = verbose
        self.api = tradeapi.REST(base_url = base_url, key_id=key_id, secret_key= secret_key, api_version='v2')
        self.account = self.api.get_account()
        if self.verbose: logging.info('Connected to Alpaca, account # {}, equity is {:,.1f}$'.format(self.account.account_number, self.getvalue()))

    def buy(self, ticker, size, kwargs):
        self._execute_order(ticker=ticker, size=size, side='buy', kwargs=kwargs)

    def sell(self, ticker, size, kwargs):
        self._execute_order(ticker=ticker, size=size, side='sell', kwargs=kwargs)

    def _execute_order(self, ticker, size, side, kwargs):
        try:
            tif = 'day'
            if 'exectype' in kwargs.keys():
                type = kwargs['exectype']
                limit_price = kwargs['price']
                self.api.submit_order( symbol=ticker, side=side, type=type, qty=int(size), time_in_force='day', limit_price=limit_price)
            else:
                type = 'market'
                self.api.submit_order( symbol=ticker, side=side, type=type, qty=int(size), time_in_force='day')
            # if self.verbose: logging.debug('Alpaca - buy {}, #{}, equity is {:,.0f}$, cash is {:,.0f}$'.format(ticker, size, self.getvalue(), self.getcash()))
        except Exception as e:
            logging.warning('[{}] exception in {},exception-{}'.format(ticker, sys._getframe().f_code.co_name, e))
