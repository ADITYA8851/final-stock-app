import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 Stock Analysis Dashboard (TradingView Style)")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, INFY.NS)", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

def calculate_macd(data, short=12, long=26, signal=9):
    exp1 = data['Close'].ewm(span=short, adjust=False).mean()
    exp2 = data['Close'].ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if symbol:
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        st.warning("No data found.")
    else:
        st.subheader(f"{symbol} Price Chart")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlestick"
        ))
        fig.update_layout(xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)

        # Add Indicators
        data['MACD'], data['Signal_Line'] = calculate_macd(data)
        data['RSI'] = calculate_rsi(data)

        st.subheader("📊 MACD Indicator")
        st.line_chart(data[['MACD', 'Signal_Line']])

        st.subheader("📈 RSI Indicator")
        st.line_chart(data[['RSI']])
