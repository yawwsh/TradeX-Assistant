

import streamlit as st
import json
import numpy as np
import ta
import websocket
import websocket_client


# Install necessary packages
import subprocess

try:
    import ta
except ImportError:
    subprocess.check_call(["pip", "install", "ta"])

try:
    import websocket
except ImportError:
    subprocess.check_call(["pip", "install", "websocket"])

try:
    import websocket_client
except ImportError:
    subprocess.check_call(["pip", "install", "websocket-client"])


try:
    import numpy
except ImportError:
    subprocess.check_call(["pip", "install", "numpy"])

# Trading Strategy Parameters
amount = 1000
core_trade_amount = amount * 0.90
core_quantity = 0
trade_amount = amount * 0.10
core_to_trade = True
transaction_cost = 0.0005
min_trade_amt = 30

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens, volumes = [], [], [], [], [], [], []
money_end = amount
candles = [opens, highs, lows, closes, volumes]

# Buy function
def buy(allocated_money, price):
    global portfolio, money_end
    quantity = allocated_money / price
    money_end = money_end - allocated_money - transaction_cost * allocated_money
    portfolio += quantity
    if investment == []:
        investment.append(allocated_money)
    else:
        investment.append(allocated_money)
        investment[-1] += investment[-2]

# Sell function
def sell(allocated_money, price):
    global portfolio, money_end
    quantity = allocated_money / price
    money_end = money_end + allocated_money - transaction_cost * allocated_money
    portfolio -= quantity
    investment.append(-allocated_money)
    investment[-1] += investment[-2]

def run_trading_bot():
    cc = 'btcusd'
    interval = '1m'

    socket = f'wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}'

    def on_close(ws):
        port_value = portfolio * closes[-1]
        if port_value > 0:
            sell(port_value, price=closes[-1])
        else:
            buy(-port_value, price=closes[-1])
        money_end += investment[-1]
        st.write('All trades settled')

    def on_message(ws, message):
        global portfolio, investment, closes, highs, lows, money_end, core_to_trade, core_quantity, real_time_portfolio_value
        json_message = json.loads(message)
        cs = json_message['k']
        candle_closed, close, high, low, open, volume = cs['x'], cs['c'], cs['h'], cs['l'], cs['o'], cs['v']
        candle = [open, high, low, close, volume]

        if candle_closed:
            for i in candles:
                i.append(float(candle[candles.index(i)]))
            st.write(f'Closes: {closes}')
            inputs = {
                'open': np.array(opens),
                'high': np.array(highs),
                'low': np.array(lows),
                'close': np.array(closes),
                'volume': np.array(volumes)
            }
            st.write(inputs)

            if core_to_trade:
                buy(core_trade_amount, price=closes[-1])
                st.write(f'Core Investment: We bought ${core_trade_amount} worth of bitcoin')
                core_quantity += core_trade_amount / closes[-1]
                core_to_trade = False

            indicators = []
            for method in ta.trend.__dir__():
                if method.startswith('cdl'):
                    indicator = getattr(ta.trend, method)(inputs)
                    indicators.append(indicator[-1])
            av_indicator = np.mean(indicators)
            st.write(av_indicator)

            if av_indicator >= 10:
                amt = trade_amount
            elif av_indicator <= -10:
                amt = -trade_amount
            else:
                amt = av_indicator * 10
            port_value = portfolio * closes[-1] - core_quantity * closes[-1]
            trade_amt = amt - port_value
            RT_portfolio_value = money_end + portfolio * closes[-1]
            real_time_portfolio_value.append(float(RT_portfolio_value))
            st.write(f'Average of all indicators is "{av_indicator}" and recommended exposure is "${amt}"')
            st.write(f'Real-Time Portfolio Value: ${RT_portfolio_value}')
            st.write(f'Invested amount: ${portfolio*closes[-1]}')

            if trade_amt > min_trade_amt:
                buy(trade_amt, price=closes[-1])
                st.write(f'We bought ${trade_amt} worth of bitcoin')
            elif trade_amt < -min_trade_amt:
                sell(-trade_amt, price=closes[-1])
                st.write(f'We sold ${-trade_amt} worth of bitcoin')

    ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
    ws.run_forever()

def main():
    st.title("Trading Bot Deployment")

    if st.button("Run Trading Bot"):
        run_trading_bot()

if __name__ == '__main__':
    main()

