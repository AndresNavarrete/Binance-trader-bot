from Bot.ConectionManager import ConectionManager

conectionManager = ConectionManager()
conectionManager.ws.run_forever()
