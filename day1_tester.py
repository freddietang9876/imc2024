#!/usr/bin/env python3
from datamodel import Listing, OrderDepth, Trade, TradingState
from day1 import Trader
from collections import Counter, defaultdict

import argparse
import pandas as pd
import numpy as np
import json

POSITION_MAX = 10
POSITION_MIN = -10

# Calculates current orders based on record data
def get_order_depths(records):
    buys = dict()
    sells = dict()

    for record in records:
        price = int(record['price'])
        quantity = int(record['quantity'])
        symbol = record['symbol']

        if (symbol not in sells) or (symbol not in buys):
            buys[symbol] = Counter()
            sells[symbol] = Counter()

        # This is an ask order
        if np.random.choice([False, True]):
            sells[symbol][price] += -quantity
        # This is a bid order
        else:
            buys[symbol][price] += quantity

    order_depths = dict()

    for symbol in ["AMETHYSTS", "STARFRUIT"]:
        order_depths[symbol] = OrderDepth(
            buy_orders=buys.get(symbol, dict()),
            sell_orders=sells.get(symbol, dict())
        )

    return order_depths

def trade_strs(X):
    return "\n".join([str(x) for Y in X.values() for x in Y])

# Runs the simulation using the data given in the dataframe.
def run_simulation(df: pd.DataFrame):
    listings = {
        "AMETHYSTS": Listing("AMETHYSTS", "AMETHYSTS", "SEASHELLS"),
        "STARFRUIT": Listing("STARFRUIT", "STARFRUIT", "SEASHELLS")
    }

    position = { "AMETHYSTS": 0, "STARFRUIT": 0 }

    traderData = None
    own_trades = dict()
    observations = dict()
    pnl = 0
    market_trades = dict()
    trader = Trader()
    out = defaultdict(list)

    for timestamp, rows in df.groupby(by="timestamp"):
        # heads = bid order, not heads = ask order
        records = rows.to_dict('records')
        order_depths = get_order_depths(records)

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

        result, conversions, traderData = trader.run(state)
        # Execute
        marginal_profit = 0
        own_trades = { "AMETHYSTS": [], "STARFRUIT": [] }

        for x in result.values():
            for trader_order in x:
                # Check if this is a BUY or a SELL
                symbol, price, quantity = trader_order.symbol, trader_order.price, trader_order.quantity
                current_position = position[symbol]

                if quantity < 0: # this is a SELL
                    actual_quantity = -quantity

                    # highest to lowest buy prices
                    buys = list(order_depths[symbol].buy_orders.items())
                    buys.sort(reverse=True)

                    # check to see if each trade can be executed
                    i = 0
                    while i < len(buys):
                        p, q = buys[i]

                        if q == 0:
                            i += 1
                            continue
                        if current_position == -20:
                            break
                        if actual_quantity == 0:
                            break

                        marginal_profit += p
                        current_position -= 1
                        actual_quantity -= 1
                        own_trades[symbol].append(Trade(
                            symbol=symbol,
                            price=p,
                            quantity=1,
                            buyer="MARKET",
                            seller="US",
                            timestamp=timestamp
                        ))
                        buys[i] = (p, q-1)

                    position[symbol] = current_position

                else: # this is a BUY
                    actual_quantity = quantity

                    # lowest to highest SELL prices
                    sells = list(order_depths[symbol].sell_orders.items())
                    sells.sort()

                    i = 0
                    while i < len(sells):
                        p, q = sells[i]
                        q = -q

                        if q == 0:
                            i += 1
                            continue
                        if current_position == 20:
                            break
                        if actual_quantity == 0:
                            break

                        marginal_profit -= p
                        current_position += 1
                        actual_quantity -= 1
                        own_trades[symbol].append(Trade(
                            symbol=symbol,
                            price=p,
                            quantity=1,
                            buyer="US",
                            seller="MARKET",
                            timestamp=timestamp
                        ))
                        sells[i] = (p, -(q-1))

                    position[symbol] = current_position

        pnl += marginal_profit

        out['timestamp'].append(timestamp)
        out['marginal_profit'].append(marginal_profit)
        out['pnl'].append(pnl)
        out['trades'].append(trade_strs(own_trades))
        out['position'].append(json.dumps(position))

    return pd.DataFrame(dict(out))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tests the trader for day 1 of Prosperity 2")
    parser.add_argument("trades", help="Path to the trades file")
    parser.add_argument("prices", help="Path to the prices file")

    args = parser.parse_args()
    trades_path = args.trades
    prices_path = args.prices

    # Read
    out = run_simulation(pd.read_csv(trades_path, sep=";"))
    prices = pd.read_csv(prices_path, sep=";")

    starfruit_midprice = 0
    amethyst_midprice = 0
    actual_pnls = []
    amethyst_midprices = []
    starfruit_midprices = []

    for _, out_row in out.iterrows():
        timestamp = out_row['timestamp']
        pnl = int(out_row['pnl'])
        prices_rows = prices.loc[prices['timestamp'] == timestamp]

        for _, prices_row in prices_rows.iterrows():
            if prices_row['product'] == "AMETHYSTS":
                amethyst_midprice = int(prices_row["mid_price"])
            else:
                starfruit_midprice = int(prices_row["mid_price"])

        position = json.loads(out_row['position'])
        actual_pnl = pnl + (starfruit_midprice * position['STARFRUIT']) + (amethyst_midprice * position['AMETHYSTS'])
        amethyst_midprices.append(amethyst_midprice)
        starfruit_midprices.append(starfruit_midprice)
        actual_pnls.append(actual_pnl)

    out['actual_pnl'] = actual_pnls
    out['starfruit_price'] = starfruit_midprices
    out['amethyst_price'] = amethyst_midprices

    out.to_csv('out.csv', index=False)