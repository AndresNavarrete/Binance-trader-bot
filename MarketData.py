from Credentials import *
from InputInformation import InputInformation

from binance.client import Client
from datetime import datetime, date, timezone
import pandas as pd


class MarketData:
    def __init__(self):
        self.inputInformation = InputInformation()
        self.historicalData = pd.DataFrame()
        self.closingPrices = pd.DataFrame()
        self.lowestPrices = pd.DataFrame()
        self.highestPrices = pd.DataFrame()
        self.lastClosedCandle = {}
        self.chooseClient()
        self.updateHistoricalData()
        self.setInitialClosingPrices()

    def chooseClient(self):
        if not self.inputInformation.isSimulation:
            self.client = Client(api_key=apiKey, api_secret=secretKey)
        else:
            self.client = Client(api_key=test_apiKey, api_secret=test_secretKey)
            self.client.API_URL = "https://testnet.binance.vision/api"

    def updateHistoricalData(self):
        candles = self.client.get_klines(
            symbol=self.inputInformation.coinSymbol.upper(),
            interval=self.inputInformation.timeInterval,
        )
        candlesDataFrame = pd.DataFrame(candles)

        closingTimeDataFrame = self.getClosingTimeFromCandles(candlesDataFrame)
        candlesDataFrame.pop(0)
        candlesDataFrame.pop(11)
        self.historicalData = candlesDataFrame.join(closingTimeDataFrame)
        self.historicalData.set_index("date", inplace=True)
        self.columnNames = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "asset_volume",
            "trade_number",
            "taker_buy_base",
            "taker_buy_quote",
        ]
        self.historicalData.columns = self.columnNames

    def getClosingTimeFromCandles(self, candlesDataFrame):
        closingTimeStamps = []
        for date in candlesDataFrame[0].unique():
            readable = datetime.fromtimestamp(int(date) / 1000)
            closingTimeStamps.append(readable)
        closingTimeDataFrame = pd.DataFrame(closingTimeStamps)
        closingTimeDataFrame.columns = ["date"]
        return closingTimeDataFrame

    def setInitialClosingPrices(self):
        self.closingPrices = self.historicalData["close"].astype("float")
        self.lowestPrices = self.historicalData["low"].astype("float")
        self.highestPrices = self.historicalData["high"].astype("float")

    def getCandlesBetweenDates(self, coin, timeInterval, dateTime1, dateTime2):
        timeStamp1 = int(datetime.timestamp(dateTime1) * 1000)
        timeStamp2 = int(datetime.timestamp(dateTime2) * 1000)
        print("Downloading info from API")
        candles = self.client.get_historical_klines(
            symbol=coin,
            interval=timeInterval,
            start_str=str(timeStamp1),
            end_str=str(timeStamp2),
            limit=1000,
        )

        backtestData = pd.DataFrame(candles)
        backtestClosingTimes = self.getClosingTimeFromCandles(backtestData)
        backtestData.pop(0)
        backtestData.pop(11)
        backtestFormatData = backtestData.join(backtestClosingTimes)
        backtestFormatData.set_index("date", inplace=True)
        backtestFormatData.columns = self.columnNames

        return backtestFormatData
