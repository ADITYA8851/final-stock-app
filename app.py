import streamlit as st
import yfinance as yf
import pandas as pd
import ta  # using the `ta` library for technical analysis

st.set_page_config(page_title="Stock Trading Dashboard", layout="wide")

st.title("📈 Stock Trading App with MACD and RSI")

# Sidebar for user input
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch data
try:
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        st.error("No data found for the selected stock and date range.")
    else:
        st.subheader(f"{symbol} Stock Data")
        st.line_chart(data["Close"])

        # Calculate Indicators
        macd_indicator = ta.trend.MACD(data["Close"])
        data["MACD"] = macd_indicator.macd()
        data["Signal_Line"] = macd_indicator.macd_signal()

        rsi_indicator = ta.momentum.RSIIndicator(data["Close"])
        data["RSI"] = rsi_indicator.rsi()

        # Display indicators
        st.subheader("MACD & Signal Line")
        if "MACD" in data.columns and "Signal_Line" in data.columns:
            st.line_chart(data[["MACD", "Signal_Line"]])
        else:
            st.warning("MACD or Signal Line not available.")

        st.subheader("RSI")
        if "RSI" in data.columns:
            st.line_chart(data["RSI"])
        else:
            st.warning("RSI not available.")
except Exception as e:
    st.error(f"Something went wrong: {e}")
