import ta

class MarketIndicators:

    def __init__(self,market):
        self.market = market
        
        self.RSI = self.calculateRSI(self.market.closingPrices)
        self.EMA10 = self.calculateEMA(self.market.closingPrices, 10)
        self.EMA20 = self.calculateEMA(self.market.closingPrices, 20)
        self.EMA200 = self.calculateEMA(self.market.closingPrices,200)
        self.MACD, self.signal = self.calculateMACD_Signal(self.market.closingPrices)
        self.minimalLowestPrice = self.calculateRecentLowestPrice(self.market.lowestPrices)
        self.maximalHighestPrice =self.calculateRecentHighestPrice(self.market.highestPrices)
        self.stochastic = self.calculateStochastic(self.market.closingPrices,
                                                    self.market.lowestPrices, 
                                                    self.market.highestPrices)
        self.stochastic_7 = self.calculate_k_Stochastics(7, self.market.closingPrices,
                                                    self.market.lowestPrices, 
                                                    self.market.highestPrices)
        self.ATR = self.calculateATR(self.market.closingPrices,
                                     self.market.lowestPrices, 
                                     self.market.highestPrices)
    
    def __str__(self):
        output = "\n\tIndicators: "
        output += "\n\tEMA10 = {}".format(self.EMA10)
        output += "\n\tEMA20 = {}".format(self.EMA20)
        output += "\n\tEMA200 = {}".format(self.EMA200)
        output += "\n\tMinimal Previous Price = {}".format(self.minimalLowestPrice)
        output += "\n\tRSI = {}".format(self.RSI)
        output += "\n\tATR = {}".format(self.ATR)
        output += "\n\tMACD = {}".format(self.MACD)
        return output

    def updateAllIndicators(self, closePrices, lowestPrices, highestPrices):
        self.RSI = self.calculateRSI(closePrices)
        self.EMA10 = self.calculateEMA(closePrices, 10)
        self.EMA20 = self.calculateEMA(closePrices, 20)
        self.EMA200 = self.calculateEMA(closePrices,200)
        self.MACD, self.signal = self.calculateMACD_Signal(closePrices)
        self.stochastic = self.calculateStochastic(closePrices, lowestPrices, highestPrices)
        self.stochastic_7 = self.calculate_k_Stochastics(7 ,closePrices, lowestPrices, highestPrices)
        self.ATR = self.calculateATR(closePrices, lowestPrices, highestPrices)
        self.minimalLowestPrice = self.calculateRecentLowestPrice(lowestPrices)
        self.maximalHighestPrice = self.calculateRecentHighestPrice(highestPrices)


    def calculateRSI(self,closePrices):
        periodsConsidered = 14
        rsi = ta.momentum.RSIIndicator(closePrices,periodsConsidered).rsi()
        return rsi[-1]

    def calculateEMA(self, closePrices, periodsConsidered):
        ema = ta.trend.EMAIndicator(closePrices, periodsConsidered).ema_indicator()
        return ema[-1]

    def calculateMACD_Signal(self, closePrices):
        macdTrend = ta.trend.MACD(closePrices, window_fast =12, window_slow =26, window_sign =9)
        macd = macdTrend.macd()
        macdsignal = macdTrend.macd_signal()
        return macd[-1] , macdsignal[-1]

    def calculateATR(self,closePrices,lowestPrices,highestPrices):
        periodsConsidered = 14
        atr = ta.volatility.AverageTrueRange(highestPrices, lowestPrices, closePrices, periodsConsidered).average_true_range()
        return atr[-1]
    
    def calculateStochastic(self,closePrices,lowestPrices,highestPrices):
        return self.calculate_k_Stochastics( 1 , closePrices ,lowestPrices, highestPrices)

    def calculate_k_Stochastics(self, k , closePrices,lowestPrices,highestPrices):
        stoch = ta.momentum.stoch_signal(highestPrices, lowestPrices, closePrices,
                                window=14,  smooth_window=3)
        return stoch[-k:]

    def calculateRecentLowestPrice(self,lowestPrices):
        periodsConsidered = 14
        lowestPrices = lowestPrices[-periodsConsidered:]
        return min(lowestPrices)
    
    def calculateRecentHighestPrice(self,highestPrices):
        periodsConsidered = 14
        highestPrices = highestPrices[-periodsConsidered:]
        return max(highestPrices)