__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
                    "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"

import logging, sys, os
import time
from configparser import ConfigParser
import pandas as pd
from alpaca_broker import AlpacaLiveBroker


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y[%H:%M:%S]',
                        handlers=[logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + '.txt'),
                                  logging.StreamHandler(sys.stdout)])
    logging.getLogger().setLevel(logging.DEBUG)

    config = ConfigParser()
    config.read('main_cfg.txt')
    trades_filename = 'trades.csv'
    if os.path.exists(trades_filename):
        # connect to Alpaca
        key_id = config.get(section='BROKER', option='key_id')
        secret_key = config.get(section='BROKER', option='secret_key')
        alpaca = AlpacaLiveBroker(key_id=key_id, secret_key=secret_key)

        # process requests
        trade_info_df = pd.read_csv(trades_filename, index_col=None)
        for tidx in range(len(trade_info_df)):
            trade_info = trade_info_df.iloc[tidx]
            logging.debug('[{}] processing {} order to {} # {}'.format(trade_info['Symbol'], trade_info['Order Type'], trade_info['Action'], trade_info['Quantity']))

            kwargs = {}
            if 'LMT' == trade_info['Order Type']:
                kwargs['exectype'] = 'limit'
                kwargs['price'] = trade_info['Lmt Price']

            if 'buy' == trade_info['Action']:
                alpaca.buy(ticker=trade_info['Symbol'], size=trade_info['Quantity'], kwargs=kwargs)
            else:
                alpaca.sell(ticker=trade_info['Symbol'], size=trade_info['Quantity'], kwargs=kwargs)
            time.sleep(3)
    else:
        logging.debug('unable to find {}, quitting'.format(trades_filename))
