from datamodel import OrderDepth, UserId, TradingState, Order, Position
from typing import List
import string


class Trader:
    def amethysts(self, amethysts: OrderDepth, pos: Position):
        result = []
        mn=1000000
        mx=0

        #BUY
        for price,quant in amethysts.sell_orders.items():
            if price<mn:
                mn=price
        netB=0
        # pos=state.position.get("AMETHYSTS",0)
        if (mn<10000-max(0,pos//4) and pos<20):
            netB=min(-amethysts.sell_orders[mn],min(20-pos,4))
            result.append(Order("AMETHYSTS",mn,netB))

        if (pos+netB<10):
            result.append(Order("AMETHYSTS", min(mn,10000)-1, (10-pos-netB)//3))

        #SELL
        for price, quant in amethysts.buy_orders.items():
            if price > mx:
                mx = price
        netS=0
        if (mx > 10000 - min(0, pos // 4) and pos > -20):
            netS = -min(amethysts.buy_orders[mx], min(pos+20,4))
            result.append(Order("AMETHYSTS", mx, netS))

        if (pos + netS > -10):
            result.append(Order("AMETHYSTS", max(mx,10000)+1, -((10+pos+netS)//3)))

        return result

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        amethystResults = self.amethysts(
            state.order_depths.get("AMETHYSTS"),
            state.position.get("AMETHYSTS")
        )
        result = {"AMETHYSTS":amethystResults}
        traderData = ""  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        print(result)
        print(state.own_trades)
        conversions = 0
        return result, conversions, traderData