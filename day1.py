from datamodel import OrderDepth, UserId, TradingState, Order, Position
import jsonpickle
from typing import List
import string


class Trader:
    def getMax(self, orders,mx=0):
        for price, quant in orders.items():
            if price > mx:
                mx = price
        return mx
    def getMin(self, orders,mn=100000):
        for price, quant in orders.items():
            if price < mn:
                mn = price
        return mn
    def amethysts(self, amethysts: OrderDepth, pos: Position):
        result = []
        mn=1000000
        mx=0

        #BUY

        mn= self.getMin(amethysts.sell_orders)
        netB=0
        sell_prices=[]
        for price,quant in amethysts.sell_orders.items():
            sell_prices.append(price)
        sell_prices.sort()
        for price in sell_prices:
            if (pos+netB>=20):
                break
            if (price<10000):
                result.append(Order("AMETHYSTS", price, min(20-pos-netB,-amethysts.sell_orders[price])))
                netB+=min(20-pos-netB,-amethysts.sell_orders[price])

    #    if (mn<10000-max(0,pos//4) and pos<20):
     #       netB=min(-amethysts.sell_orders[mn],20-pos)
      #      result.append(Order("AMETHYSTS",mn,netB))

        if (pos+netB<20):
            result.append(Order("AMETHYSTS", 9999, max(1,(20-pos-netB)-1)))

        #SELL
        mx = self.getMax(amethysts.buy_orders)
        netS=0

        buy_prices = []
        for price, quant in amethysts.buy_orders.items():
            buy_prices.append(price)
        buy_prices.sort()
        buy_prices.reverse()
        for price in buy_prices:
            if (pos + netS <= -20):
                break
            if (price > 10000):
                # print(price,netS,-min(amethysts.buy_orders[mx], pos+netS+20))
                result.append(Order("AMETHYSTS", price, -min(amethysts.buy_orders[price], pos+netS+20)))
                netS += -min(amethysts.buy_orders[price], pos+netS+20)
                # print(netS)
        # if (mx > 10000 - min(0, pos // 4) and pos > -20):
        #     netS = -min(amethysts.buy_orders[mx], pos+20)
        #     result.append(Order("AMETHYSTS", mx, netS))

        if (pos + netS > -20):
            result.append(Order("AMETHYSTS", 10001, -(max(1,(20+pos+netS)-1))))

        return result
    def starfruit(self, starfruit: OrderDepth, pos: Position, tradeData):
        coeffs= [0.18898843, 0.20770677, 0.26106908, 0.34176867]
        intercept = 2.3564943532519464
        orders = []
        prices=[]
        if (not tradeData):
            prices=[5053.5,5049.5,5051]
        else:
            prices = tradeData
        mn=self.getMin(starfruit.buy_orders)
        mx=self.getMax(starfruit.sell_orders)
        current_mid = abs(mx+mn)/2
        prices.append(current_mid)
        # print(prices)
        next_price= sum([prices[i]*coeffs[i] for i in range(len(coeffs))])+intercept
        # print(next_price)
        #BUY
        mn = self.getMin(starfruit.sell_orders)
        netB = 0

        if (mn < next_price - max(0, pos // 4) and pos < 20):
            netB = min(-starfruit.sell_orders[mn], min(20 - pos, 4))
            orders.append(Order("STARFRUIT", mn, netB))
        if (pos+netB<10):
            orders.append(Order("STARFRUIT", min(mn,int(next_price))-1, (10-pos-netB)//3))

        #SELL
        mx = self.getMax(starfruit.buy_orders)
        netS = 0
        if (mx > next_price - min(0, pos // 4) and pos > -20):
            netS = -min(starfruit.buy_orders[mx], min(pos + 20, 4))
            orders.append(Order("STARFRUIT", mx, netS))

        if (pos + netS > -10):
            orders.append(Order("STARFRUIT", max(mx, int(next_price)+1) + 1, -((10 + pos + netS) // 3)))
        newTradeData=prices[1:]
        return orders,newTradeData
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        starfruit = []
        tradeData={}
        if (state.traderData):
            tradeData = jsonpickle.decode(state.traderData)
            starfruit=tradeData["STARFRUIT"]



        amethystResults = self.amethysts(
            state.order_depths.get("AMETHYSTS",{}),
            state.position.get("AMETHYSTS",0)
        )
        starFruitResults,starFruitData = self.starfruit(state.order_depths.get("STARFRUIT",{}),state.position.get("STARFRUIT",0),starfruit)
        result = {"AMETHYSTS":amethystResults,"STARFRUIT":starFruitResults}
       # result = {"AMETHYSTS": amethystResults}
        #return result,0,""
       # print(starFruitData)
        conversions = 0

        return result, conversions, jsonpickle.encode({"STARFRUIT":starFruitData})
