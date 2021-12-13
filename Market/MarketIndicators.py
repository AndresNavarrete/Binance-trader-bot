import ta


class MarketIndicators:
    def __init__(self, market):
        self.market = market
        self.RSI = self.calculateRSI(self.market.closingPrices)

    def __str__(self):
        output = "\n\tIndicators: "
        output += "\n\tRSI = {}".format(self.RSI)
        return output

    def updateAllIndicators(self, closePrices, lowestPrices, highestPrices):
        self.RSI = self.calculateRSI(closePrices)
        
    def calculateRSI(self, closePrices):
        periodsConsidered = 14
        rsi = ta.momentum.RSIIndicator(closePrices, periodsConsidered).rsi()
        return rsi[-1]
