from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string


class Trader:

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {"AMETHYSTS":[]}
        amethysts=state.order_depths["AMETHYSTS"]
        avg=0
        num=0
        if (state.traderData != ""):
            avg=int(state.traderData.split(" ")[0])
            num = int(state.traderData.split(" ")[1])
        mn=1000000
        mx=0
        #BUY
        for price,quant in amethysts.sell_orders.items():
            if price<mn:
                mn=price
        netB=0
        pos=state.position["AMETHYSTS"]
        if (mn<10000+min(0,pos//4) and pos<20):
            netB=min(-amethysts.sell_orders[mn],min(20-pos,4))
            result["AMETHYSTS"].append(Order("AMETHYSTS",mn,netB))

        if (pos+netB<10):
            result["AMETHYSTS"].append(Order("AMETHYSTS", min(mn,10000)-1, (10-pos-netB)//3))
        #SELL
        for price, quant in amethysts.buy_orders.items():
            if price > mx:
                mx = price
        netS=0
        if (mx > 10000 + max(0, pos // 4) and pos > -20):
            netS = min(amethysts.buy_orders[mx], -min(pos+20,4))
            result["AMETHYSTS"].append(Order("AMETHYSTS", mx, -netS))

        if (pos - netS > -10):
            result["AMETHYSTS"].append(Order("AMETHYSTS", max(mx,10000)+1, -((10+pos+netS)//3)))
        traderData = ""  # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.

        conversions = 0
        return result, conversions, traderData