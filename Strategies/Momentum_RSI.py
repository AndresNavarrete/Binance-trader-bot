class Momentum_RSI:
    def __init__(self):
        self.currentPrice = None
        self.indicators = None
        self.codeName = "Momentum_RSI"
        self.lastOpenTrend = None
        self.stopLoss = None
        self.takeProfitPrice = None
        self.response = {}

    def execute(self, indicators, price, wallet):
        self.indicators = indicators
        self.currentPrice = price
        self.resetResponse()
        currentCurrency = self.getCurrencyFromWallet(wallet)
        self.setNewResponse(indicators, wallet, currentCurrency)

        return self.response

    def resetResponse(self):
        self.response = {
            "trade": False,
            "operation": None,
            "dolarsToSell": 0,
            "cryptoToSell": 0,
        }

    def getCurrencyFromWallet(self, wallet):
        if wallet["dolars"] < 5:
            return "crypto"
        return "dolars"

    def setNewResponse(self, indicators, wallet, currentCurrency):
        upperLimit = 70
        lowerLimit = 30

        if indicators.RSI < upperLimit and indicators.RSI > lowerLimit:
            return

        if indicators.RSI >= upperLimit and currentCurrency == "crypto":
            self.provideTradeInformation(wallet, operation="Sell")

        elif indicators.RSI <= lowerLimit and currentCurrency == "dolars":
            self.provideTradeInformation(wallet, operation="Buy")

    def provideTradeInformation(self, wallet, operation):
        self.response["trade"] = True

        if operation == "Buy":
            self.response["operation"] = operation
            self.response["dolarsToSell"] = wallet["dolars"]
        elif operation == "Sell":
            self.response["operation"] = operation
            self.response["cryptoToSell"] = wallet["crypto"]

    def resetEnvironment(self):
        self.currentPrice = None
        self.indicators = None
