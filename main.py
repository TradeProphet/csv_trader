import logging, sys, os
import time
from configparser import ConfigParser
import pandas as pd
import ib_bridge
import datetime


pd.set_option('mode.chained_assignment', None)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y[%H:%M:%S]',
                        handlers=[logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + '.txt'),
                                  logging.StreamHandler(sys.stdout)])
    logging.getLogger().setLevel(logging.DEBUG)

    config = ConfigParser()
    config.read('main_cfg.txt')
    trades_filename = 'trades.csv'
    if os.path.exists(trades_filename):
        trade_info_df = pd.read_csv(trades_filename, index_col=None)
        # connect to IB
        portid = config.getint(section='IB', option='port')
        account = config.get(section='IB', option='account')
        clientid = config.get(section='IB', option='clientid')
        ib = ib_bridge.ib_bridge(ipaddress='127.0.0.1', portid=portid, clientid=clientid, account=account)
        # process requests
        for tidx in range(len(trade_info_df)):
            trade_info = trade_info_df.iloc[tidx]
            logging.debug('[{}] processing {} order to {} # {}'.format(trade_info['Symbol'], trade_info['Entry Order Type'], trade_info['Action'], trade_info['Quantity']))
            trade_info['Entry time'] = None if pd.isnull(trade_info['Entry time']) else datetime.datetime.now().\
                replace(hour=int(trade_info['Entry time'].split(':')[0]),
                minute=int(trade_info['Entry time'].split(':')[1]),
                second=int(trade_info['Entry time'].split(':')[2]), microsecond=00)
            trade_info['Exit order'] = None if pd.isnull(trade_info['Exit order']) else trade_info['Exit order']
            trade_info['Entry Lmt Price'] = None if pd.isnull(trade_info['Entry Lmt Price']) else trade_info['Entry Lmt Price']
            trade_info['Exit Lmt Price'] = None if pd.isnull(trade_info['Exit Lmt Price']) else trade_info['Exit Lmt Price']
            trade_info['Exit time'] = None if pd.isnull(trade_info['Exit time']) else datetime.datetime.now().\
                replace(hour=int(trade_info['Exit time'].split(':')[0]),
                minute=int(trade_info['Exit time'].split(':')[1]),
                second=int(trade_info['Exit time'].split(':')[2]), microsecond=00)
            exit_order = {'orderType':trade_info['Exit order'], 'lmtPrice':trade_info['Exit Lmt Price'], 'goodAfterTime':trade_info['Exit time']}
            ib.execute_order(symbol=trade_info['Symbol'], secType=trade_info['Type'], exchange=trade_info['Exchange'],
                            currency=trade_info['Currency'], action=trade_info['Action'], quantity=trade_info['Quantity'],
                            orderType=trade_info['Entry Order Type'], lmtPrice=trade_info['Entry Lmt Price'],
                            tif=trade_info['Time in Force'], goodAfterTime=trade_info['Entry time'],
                            goodTillDate=None, exit_order=exit_order)
            time.sleep(3)

        ib.terminate()
    else:
        logging.debug('unable to find {}, quitting'.format(trades_filename))
