# CSV Trader

This Python script reads trades description in a CSV file and executes them on the Alpaca broker

A paper account for Alpaca can be opened easily https://Alpaca.markets

## The CSV file contains:
**Symbol** - the ticker symbol to trade

**Action** - buy or sell

**Quantity** - the size to trade

**Order Type** - 'market' for market order, 'limit' for limit order type

**Lmt Price** - limit threshold to use for LMT order type

**Stop Loss** - stop loss used for execution

**Take Profit** - take profit target

## Connecting to Alpaca
main_cfg.txt file contains the required key id and secret key used to connect to Alpaca
Once you signed up to Alpaca , go the the main page to generate these and copy paste 
to the main_cfg.txt file

### Usage
You are free to use the code in any way you like,

**If you have questions shoot me an email Alon@AlphaOverBeta.net**

Trade smartly,

Alon