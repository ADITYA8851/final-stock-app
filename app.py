import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from pandas_ta.trend import macd
from pandas_ta.momentum import rsi

st.set_page_config(layout="wide")

st.title("📈 Stock Trading View-Like Dashboard")

# Input section
stock = st.text_input("Enter stock symbol (e.g., AAPL, TSLA, INFY.NS):", value="AAPL")
interval = st.selectbox("Select interval:", ["1d", "1h", "30m", "15m", "5m"])

# Map interval to period for yfinance
range_map = {"1d": "1mo", "1h": "1mo", "30m": "3mo", "15m": "1mo", "5m": "10d"}
period = range_map.get(interval, "1mo")

try:
    data = yf.download(stock, period=period, interval=interval)

    if data.empty:
        st.error("No data found. Try a different stock symbol or interval.")
    else:
        st.subheader(f"Stock Data: {stock.upper()} - Interval: {interval}")

        # Display candlestick chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'],
                                     name='Candlesticks'))
        fig.update_layout(xaxis_rangeslider_visible=False,
                          height=500,
                          margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

        # Calculate RSI
        data['RSI'] = rsi(data['Close'], length=14)
        if data['RSI'].notna().sum() > 10:
            st.subheader("RSI Indicator")
            st.line_chart(data['RSI'], use_container_width=True)
        else:
            st.warning("RSI data not available (not enough data).")

        # Calculate MACD
        macd_result = macd(data['Close'])
        if not macd_result.empty:
            data['MACD'] = macd_result['MACD_12_26_9']
            data['Signal_Line'] = macd_result['MACDs_12_26_9']

            macd_points = data['MACD'].notna().sum()
            st.text(f"MACD points available: {macd_points}")

            if macd_points > 10:
                st.subheader("MACD Indicator")
                st.line_chart(data[['MACD', 'Signal_Line']], use_container_width=True)
            else:
                st.warning("MACD/Signal Line not available (not enough data).")
        else:
            st.warning("MACD calculation returned no results.")

except Exception as e:
    st.error(f"Error loading data: {e}")
