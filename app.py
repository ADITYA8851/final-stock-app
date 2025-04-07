import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Manual RSI
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Manual MACD
def compute_macd(series, short=12, long=26, signal=9):
    exp1 = series.ewm(span=short, adjust=False).mean()
    exp2 = series.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# Streamlit UI
st.set_page_config(page_title="Stock Trading App", layout="wide")
st.title("📊 Stock Trading Dashboard")

# Sidebar Inputs
st.sidebar.title("Stock Selector")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL").upper()
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "30m", "15m", "5m"], index=0)
range_map = {"1d": "5d", "1h": "7d", "30m": "1mo", "15m": "1mo", "5m": "5d"}
period = range_map[interval]

# Download data
data = yf.download(ticker, period=period, interval=interval)
stock = yf.Ticker(ticker)
info = stock.info
name = info.get("shortName", "Unknown Company")
price = info.get("regularMarketPrice", 0)

# Show basic info
st.subheader(f"📌 {name} ({ticker})")
st.metric(label="Current Price", value=f"${price:.2f}")

# Add RSI and MACD
data['RSI'] = compute_rsi(data['Close'])
data['MACD'], data['Signal_Line'] = compute_macd(data['Close'])

# Candlestick chart
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name="Candlestick"
))
fig.update_layout(title=f"{ticker} Price Chart ({interval})", template="plotly_dark", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# Technical Indicator Charts
st.subheader("📉 Technical Indicators")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(data['RSI'], use_container_width=True)
    st.caption("Relative Strength Index (RSI)")

with col2:
    st.line_chart(data[['MACD', 'Signal_Line']], use_container_width=True)
    st.caption("MACD & Signal Line")
