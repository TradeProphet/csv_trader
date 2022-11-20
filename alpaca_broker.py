import logging
import alpaca_trade_api as tradeapi
import sys


logging.getLogger("urllib3").setLevel(logging.WARNING)


class AlpacaLiveBroker:
    def __init__(self, key_id, secret_key, verbose=True, base_url = 'https://paper-api.alpaca.markets'):
        '''
        initialize the alpaca API connection
        :param key_id: Alpaca key id
        :param secret_key: Alpaca secret key
        :param verbose: True for printouts while managing connection
        :param base_url: paper or live trade
        '''
        self.verbose = verbose
        self.api = tradeapi.REST(base_url = base_url, key_id=key_id, secret_key= secret_key, api_version='v2')
        self.account = self.api.get_account()
        if self.verbose: logging.info('Connected to Alpaca, account # {}'.format(self.account.account_number))

    def buy(self, ticker, size, kwargs):
        '''
        buy a stock on Alpaca broker
        :param ticker: the stock ticker
        :param size: size to buy
        :param kwargs: addition parameters
        :return: NA
        '''
        self._execute_order(ticker=ticker, size=size, side='buy', kwargs=kwargs)

    def sell(self, ticker, size, kwargs):
        '''
        buy a stock on Alpaca broker
        :param ticker: the stock ticker
        :param size: size to buy
        :param kwargs: addition parameters
        :return: NA
        '''
        self._execute_order(ticker=ticker, size=size, side='sell', kwargs=kwargs)

    def _execute_order(self, ticker, size, side, kwargs):
        '''
        an internal method to handle buy / sell trades
        :param ticker: the stock ticker
        :param size: size to buy
        :param side: 'buy' or 'sell'
        :param kwargs: addition parameters
        :return: NA
        '''
        try:
            stop_loss = None
            if kwargs['stop_loss'] is not None:
                stop_loss = dict(stop_price='{:.2f}'.format(kwargs['stop_loss']))

            take_profit = None
            if kwargs['take_profit'] is not None:
                take_profit = dict(stop_price='{:.2f}'.format(kwargs['take_profit']))

            type = 'market'
            limit_price = None
            if 'exectype' in kwargs.keys():
                type = kwargs['exectype']
                if 'limit' == kwargs['exectype']:
                    limit_price = kwargs['price']
            self.api.submit_order( symbol=ticker, side=side, type=type, qty=int(size), limit_price=limit_price,
                stop_loss=stop_loss, take_profit=take_profit)
            if self.verbose:
                logging.debug('Alpaca - {} {} {}, #{}'.format(ticker, side, type, size))
        except Exception as e:
            logging.exception(str(e))
