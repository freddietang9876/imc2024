from datamodel import Listing, OrderDepth, Trade, TradingState
from day1 import Trader
import jsonpickle
timestamp = 1000

listings = {
	"PRODUCT1": Listing(
		symbol="PRODUCT1",
		product="PRODUCT1",
		denomination= "SEASHELLS"
	),
	"STARFRUIT": Listing(
		symbol="STAFRUIT",
		product="PRODUCT2",
		denomination= "SEASHELLS"
	),
}

order_depths = {
	"AMETHYSTS": OrderDepth(
		buy_orders={10001: 18,10002:5, 9999: 5},
		sell_orders={9998: -7, 10002: -8}
	),
	"STARFRUIT": OrderDepth(
		buy_orders={5036: 30},
		sell_orders={5043: -30, 5044: -8}
	),
}

own_trades = {
	"PRODUCT1": [],
	"PRODUCT2": []
}

market_trades = {
	"PRODUCT1": [
		Trade(
			symbol="PRODUCT1",
			price=11,
			quantity=4,
			buyer="",
			seller="",
			timestamp=900
		)
	],
	"PRODUCT2": []
}

position = {
	"AMETHYSTS": 0,
	"STARFRUIT": 0
}

observations = {}
traderData = jsonpickle.encode({"STARFRUIT":[5040,5050,5060]})

state = TradingState(
	traderData,
	timestamp,
    listings,
	order_depths,
	own_trades,
	market_trades,
	position,
	observations
)
trader=Trader()
result,_,data=trader.run(state)
print("data:",data)
print(result)