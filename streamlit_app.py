import streamlit as st
import pandas as pd
import requests
import time

# Define the trading strategy
def buy_btc():
  """Buys BTC if the price is above the moving average."""
  price = get_btc_price()
  moving_average = get_moving_average()
  if price > moving_average:
    st.write("Buying BTC!")

def sell_btc():
  """Sells BTC if the price is below the moving average."""
  price = get_btc_price()
  moving_average = get_moving_average()
  if price < moving_average:
    st.write("Selling BTC!")

# Get the current BTC price
def get_btc_price():
  response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
  data = response.json()
  return data["amount"]

# Get the moving average
def get_moving_average():
  data = pd.read_csv("btc_price_data.csv")
  moving_average = data["Close"].rolling(window=10).mean()
  return moving_average[-1]

# Create the Streamlit app
st.title("BTC Trading Bot")

# Run the trading strategy
if st.button("Buy BTC"):
  buy_btc()

if st.button("Sell BTC"):
  sell_btc()
