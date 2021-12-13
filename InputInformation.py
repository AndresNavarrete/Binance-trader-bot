from Strategies.Momentum_RSI import Momentum_RSI

class InputInformation:

    def __init__(self):
        self.strategy =  Momentum_RSI()
        self.firstCoin ="eth"
        self.secondCoin ="usdt"
        self.timeInterval = '1m'
        self.isSimulation = False
        self.coinSymbol = self.firstCoin + self.secondCoin

  