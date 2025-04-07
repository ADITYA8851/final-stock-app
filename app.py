import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 Stock Analysis Dashboard (TradingView Style)")

# Input for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, INFY.NS)", "AAPL")

# Select date range
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if symbol:
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            st.warning("No data available. Please check the symbol or date range.")
        else:
            data.dropna(inplace=True)

            st.subheader(f"{symbol} Stock Chart")
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Price"
            ))

            fig.update_layout(
                xaxis_rangeslider_visible=False,
                height=600,
                margin=dict(l=20, r=20, t=30, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Calculate MACD and RSI
            macd = ta.macd(data['Close'])
            rsi = ta.rsi(data['Close'])

            # Add indicators if they exist
            if macd is not None and not macd.empty:
                data = pd.concat([data, macd], axis=1)
            else:
                st.warning("MACD data not available (not enough data).")

            if rsi is not None and not rsi.empty:
                data['RSI'] = rsi
            else:
                st.warning("RSI data not available (not enough data).")

            # Plot indicators
            if 'MACD_12_26_9' in data.columns and 'MACDs_12_26_9' in data.columns:
                st.subheader("📉 MACD Indicator")
                st.line_chart(data[['MACD_12_26_9', 'MACDs_12_26_9']])
            else:
                st.info("MACD/Signal Line not available.")

            if 'RSI_14' in data.columns:
                st.subheader("📊 RSI Indicator")
                st.line_chart(data['RSI_14'])
            else:
                st.info("RSI not available.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
