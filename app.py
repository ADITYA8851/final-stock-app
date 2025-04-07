import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta

# App Layout
st.set_page_config(page_title="Stock Tracker", layout="wide")
st.title("📊 Stock Trading Dashboard")

# Sidebar Controls
st.sidebar.title("Stock Selector")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL").upper()
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "30m", "15m", "5m"], index=0)
range_map = {"1d": "5d", "1h": "7d", "30m": "1mo", "15m": "1mo", "5m": "5d"}
period = range_map[interval]

# Get stock data
data = yf.download(ticker, period=period, interval=interval)
stock = yf.Ticker(ticker)
info = stock.info
name = info.get("shortName", "Unknown Company")
price = info.get("regularMarketPrice", 0)

# Display Info
st.subheader(f"📌 {name} ({ticker})")
st.metric(label="Current Price", value=f"${price:.2f}")

# Technical Indicators
data['RSI'] = ta.rsi(data['Close'], length=14)
macd = ta.macd(data['Close'])
data = data.join(macd)

# Candlestick Chart
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name="Candlesticks"
))
fig.update_layout(title=f"{ticker} Price Chart ({interval})", template="plotly_dark", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# RSI & MACD Charts
st.subheader("📉 Technical Indicators")

col1, col2 = st.columns(2)
with col1:
    st.line_chart(data['RSI'], use_container_width=True)
    st.caption("Relative Strength Index (RSI)")
with col2:
    st.line_chart(data[['MACD_12_26_9', 'MACDs_12_26_9']], use_container_width=True)
    st.caption("MACD and Signal Line")
