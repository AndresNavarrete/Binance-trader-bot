# Binance trader bot
### Purpose of this project
This public project is an implementation of a trading bot on Binance using a websocket connection and a simple trading strategy based on the [RSI Momentum] of a given currency. This code was written using the following  [Binance documentation].


### Requirements and use
The requirements.txt file should list all Python libraries that are mandatory for running this bot. To install them you can use:
```sh
pip install -r requirements.txt
```

The selection of the coin pair to trade and the time interval to use can be done on the `InputInformation` file. The list of symbols and time interval supported can be found in the [Binance documentation]. The `IsSimulation` attribute can be used to shift from a sandbox mode to a real trading mode.

The file `Credentials` has the api and secret key for your Binance account. If you need help with your keys, please read [How to get my keys].

To start the trading bot you just need to execute the following line:

```sh
python run.py
```


   [Binance documentation]: <https://python-binance.readthedocs.io/en/latest/>
   [How to get my keys]:  <https://www.binance.com/en/support/faq/360002502072>
   [RSI Momentum]: <https://www.thebalance.com/trading-commodities-with-rsi-and-momentum-indicators-809349>