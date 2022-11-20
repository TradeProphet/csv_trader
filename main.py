__author__ = "Alon Horesh, AlphaOverBeta"
__version__ = "0.1"
__email__ = "alon@alphaoverbeta.net"
__status__ = "Production"

'''
This script takes trades from a csv file (trades.csv) and executes the trades on Alpaca broker (Alpaca.markets)
You can easily open a paper account on Alpaca broker and try this
The order types supported are mrket and limit orders
This Python script may run before the market open as Alpaca stores the trades and execute them once the market is open
'''

import logging, sys, os
import time
from configparser import ConfigParser
import pandas as pd

from alpaca_broker import AlpacaLiveBroker
import numpy as np

if __name__ == '__main__':
    # get the log file and level
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y[%H:%M:%S]',
                        handlers=[logging.FileHandler('log.txt'),
                                  logging.StreamHandler(sys.stdout)])
    logging.getLogger().setLevel(logging.DEBUG)

    # read the Alpaca API details from a config file
    config = ConfigParser()
    config.read('main_cfg.txt')

    # fetch the trades from the csv file
    trades_filename = 'trades.csv'
    if os.path.exists(trades_filename):
        # connect to Alpaca
        key_id = config.get(section='BROKER', option='key_id')
        secret_key = config.get(section='BROKER', option='secret_key')
        alpaca = AlpacaLiveBroker(key_id=key_id, secret_key=secret_key)

        # process requests
        trade_info_df = pd.read_csv(trades_filename, index_col=None).replace(np.nan, None)
        for tidx in range(len(trade_info_df)):
            trade_info = trade_info_df.iloc[tidx]
            logging.debug('[{}] processing {} order to {} # {}'.format(trade_info['Symbol'], trade_info['Order Type'], trade_info['Action'], trade_info['Quantity']))
            # prepare the trades
            kwargs = {}
            if 'limit' == trade_info['Order Type']:
                kwargs['exectype'] = 'limit'
                kwargs['price'] = trade_info['Lmt Price']
            kwargs['stop_loss'] = trade_info['Stop Loss']
            kwargs['take_profit'] = trade_info['Take Profit']
            if 'buy' == trade_info['Action']:
                alpaca.buy(ticker=trade_info['Symbol'], size=trade_info['Quantity'], kwargs=kwargs)
            else:
                alpaca.sell(ticker=trade_info['Symbol'], size=trade_info['Quantity'], kwargs=kwargs)
            time.sleep(3)
    else:
        logging.debug('unable to find {}, quitting'.format(trades_filename))
