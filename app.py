import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# RSI function
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD function
def compute_macd(series, short=12, long=26, signal=9):
    exp1 = series.ewm(span=short, adjust=False).mean()
    exp2 = series.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# Streamlit setup
st.set_page_config(page_title="Stock Trading App", layout="wide")
st.title("📈 Stock Trading Dashboard")

# Sidebar inputs
st.sidebar.title("Choose Stock")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL").upper()
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "30m", "15m", "5m"], index=0)
range_map = {"1d": "5d", "1h": "7d", "30m": "1mo", "15m": "1mo", "5m": "5d"}
period = range_map[interval]

# Download data
data = yf.download(ticker, period=period, interval=interval)
stock = yf.Ticker(ticker)
info = stock.info
name = info.get("shortName", "N/A")
price = info.get("regularMarketPrice", 0.0)

# Show stock info
st.subheader(f"📌 {name} ({ticker})")
st.metric(label="Current Price", value=f"${price:.2f}")

# Compute indicators
if not data.empty:
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
        name="Candlesticks"
    ))
    fig.update_layout(title=f"{ticker} Price Chart", xaxis_rangeslider_visible=False, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Indicator section
    st.subheader("📊 Technical Indicators")
    col1, col2 = st.columns(2)

    with col1:
        if 'RSI' in data.columns and data['RSI'].notna().sum() > 0:
            st.line_chart(data['RSI'].dropna(), use_container_width=True)
            st.caption("Relative Strength Index (RSI)")
        else:
            st.warning("RSI not available (not enough data).")

    with col2:
        if {'MACD', 'Signal_Line'}.issubset(data.columns) and data[['MACD', 'Signal_Line']].dropna().shape[0] > 0:
            st.line_chart(data[['MACD', 'Signal_Line']].dropna(), use_container_width=True)
            st.caption("MACD & Signal Line")
        else:
            st.warning("MACD/Signal Line not available (not enough data).")
else:
    st.error("No data available. Try a different stock or interval.")
