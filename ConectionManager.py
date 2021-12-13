from binance.client import Client
from MarketData import MarketData
from InputInformation import InputInformation
from MarketIndicators import MarketIndicators
from binance.exceptions import BinanceAPIException, BinanceOrderException
import sys
import json
import websocket
from datetime import datetime

class ConectionManager:

    def __init__(self):
        self.inputInformation = InputInformation()
        self.marketData = MarketData()
        self.indicators = MarketIndicators(self.marketData)
        self.strategy = self.inputInformation.strategy
        self.client = self.marketData.client
        self.closingPrices = self.marketData.closingPrices
        self.currentPrice = self.closingPrices[-1]
        self.setWebSocket()    

    def setWebSocket(self):
        source = self.getSocketSource()
        self.ws = websocket.WebSocketApp(source,
                    on_message = lambda ws,msg: self.on_message(ws, msg),
                    on_error   = lambda ws,msg: self.on_error(ws, msg),
                    on_close   = lambda ws:     self.on_close(ws),
                    on_open    = lambda ws:     self.on_open(ws))

    def getSocketSource(self):
        if self.inputInformation.isSimulation:
            socketSource = "wss://testnet.binance.vision/ws/{}@kline_{}".format(self.inputInformation.coinSymbol,
                                                                                 self.inputInformation.timeInterval)
        else:
            socketSource = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(self.inputInformation.coinSymbol,
                                                                                    self.inputInformation.timeInterval)
        return socketSource

            
    def updateWallet(self):
        try:
            balances = self.client.get_account()['balances']
            firstCoinName = self.inputInformation.firstCoin.upper()
            secondCoinName = self.inputInformation.secondCoin.upper()

            self.wallet = {'crypto': self.getCurrencyInWallet(firstCoinName, balances),
                            'dolars': self.getCurrencyInWallet(secondCoinName, balances)}
            message = 'wallet: {}'.format(self.wallet)
        except:
            error  = sys.exc_info()[0]
            message ="Wallet error: {}".format(error)
            self.addLog(message)
        
    def getCurrencyInWallet(self,currencyName, balances):
        for currency in balances:
            if currency['asset'] == currencyName:
                return float(currency['free'])
        message = "Not found currency: {}".format(currencyName)
        self.addLog(message)

    def on_error(self, ws, error):
        message = "Error in connection: {}".format(error)
        self.addLog(message)

    def on_open(self,ws):
        message = "Opened conection"
        self.addLog(message)
        self.updateWallet()
    
    def on_message(self, ws, message):
        try: 
            self.processMessage(message)
        except:
            error  = sys.exc_info()[0]
            message = "on_message error: {}".format(error)
            self.addLog(message)

    def processMessage(self, message):
        jsonMessage = json.loads(message)
        newCandle = jsonMessage['k']
        candleIsClosed = newCandle['x']
        if candleIsClosed == False :
            return
        self.manageNewCandle(newCandle)
        self.executeTradeLogic()

    def manageNewCandle(self, newCandle):
        message = "New Candle: {}".format(newCandle)
        self.addLog(message)
        self.marketData.lastClosedCandle = newCandle
        self.currentPrice = float(newCandle['c'])
        self.updateIndicators(newCandle)
        self.updateWallet()
    
    def updateIndicators(self, newCandle):
        closePrice = float(newCandle['c'])
        lowestPrice = float(newCandle['l'])
        highestPrice = float(newCandle['h'])
        timeofClose = newCandle['T']
        readableDate = datetime.fromtimestamp(int(timeofClose+1)/1000)
        self.closingPrices.loc[readableDate] = closePrice
        self.marketData.lowestPrices.loc[readableDate] = lowestPrice
        self.marketData.highestPrices.loc[readableDate] = highestPrice
        self.indicators.updateAllIndicators(self.closingPrices,self.marketData.lowestPrices,self.marketData.highestPrices)


    def on_close(self, ws):
        message = "Closed conection"
        self.addLog(message)
    
    def executeTradeLogic(self):
        instruction = self.strategy.execute(self.indicators, self.currentPrice, self.wallet)
        message = "Instruction: {}".format(instruction)
        self.addLog(message)
        if instruction['operation']== "Buy" :
            self.pushBuyOrder(instruction)
            
        elif instruction['operation']== "Sell" :
            self.pushSellOrder(instruction)
            
        else:
            self.addLog('No transaction')

    def pushBuyOrder(self, instruction):
        symbol=self.inputInformation.coinSymbol.upper()
        quantity = instruction['dolarsToSell']  
        side='BUY'
        message = "Bot is trying to buy"
        self.addLog(message)
        try:
            order = self.client.create_order(symbol = symbol, side = side, type = 'MARKET', quoteOrderQty = quantity)
            message = "Bot has bought !!! {}".format(order)
            self.addLog(message)
            
            
        except:
            error  = sys.exc_info()[0]
            message = "Error on pushBuyOrder {}".format(error)
            self.addLog(message)
               

    def pushSellOrder(self, instruction):
        symbol=self.inputInformation.coinSymbol.upper()
        quantity = instruction['cryptoToSell']
        side='SELL'
        message = "Bot is trying to sell"
        self.addLog(message)
        try:
            order = self.client.create_order(symbol = symbol, side = side, type = 'MARKET', quantity = quantity)
            message = "Bot has sold !!! {}".format(order)
            self.addLog(message)
        except:
            error  = sys.exc_info()[0]
            message = "Error on pushSellOrder {}".format(error)
            self.addLog(message)
    
    def addLog(self, message):
        print(message) #TO DO: add real logs
