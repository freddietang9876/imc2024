from datamodel import Listing, OrderDepth, Trade, TradingState
from day1 import Trader
timestamp = 1000

listings = {
	"PRODUCT1": Listing(
		symbol="PRODUCT1",
		product="PRODUCT1",
		denomination= "SEASHELLS"
	),
	"PRODUCT2": Listing(
		symbol="PRODUCT2",
		product="PRODUCT2",
		denomination= "SEASHELLS"
	),
}

order_depths = {
	"AMETHYSTS": OrderDepth(
		buy_orders={10001: 7, 9999: 5},
		sell_orders={9998: -4, 100002: -8}
	),
	"PRODUCT2": OrderDepth(
		buy_orders={142: 3, 141: 5},
		sell_orders={144: -5, 145: -8}
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
	"PRODUCT2": -5
}

observations = {}
traderData = ""

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
result,_,__=trader.run(state)
print(result)