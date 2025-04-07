import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta  # ✅ Single import

st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")

st.title("📊 Stock Market Dashboard")
st.markdown("Analyze stock trends using technical indicators like **MACD** and **RSI**.")

# --- Sidebar ---
st.sidebar.header("🔍 Stock Selector")
stock_symbol = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# --- Data Fetch ---
@st.cache_data
def load_stock_data(symbol, start, end):
    try:
        df = yf.download(symbol, start=start, end=end)
        if not df.empty:
            return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
    return pd.DataFrame()

data = load_stock_data(stock_symbol, start_date, end_date)

if data.empty:
    st.error("No stock data found. Please try a valid ticker or change the date range.")
    st.stop()

st.subheader(f"📅 Historical Stock Data for `{stock_symbol.upper()}`")
st.dataframe(data.tail())

# --- Technical Indicators ---
st.subheader("📈 Price Chart")
st.line_chart(data['Close'])

# Calculate MACD
def calculate_macd(df):
    try:
        macd_result = ta.macd(df['Close'])
        df = pd.concat([df, macd_result], axis=1)
    except Exception as e:
        st.warning(f"MACD Calculation Failed: {e}")
    return df

# Calculate RSI
def calculate_rsi(df):
    try:
        df['RSI'] = ta.rsi(df['Close'])
    except Exception as e:
        st.warning(f"RSI Calculation Failed: {e}")
    return df

data = calculate_macd(data)
data = calculate_rsi(data)

# --- MACD Plot ---
st.subheader("🔻 MACD Indicator")
if 'MACD_12_26_9' in data.columns and 'MACDs_12_26_9' in data.columns:
    st.line_chart(data[['MACD_12_26_9', 'MACDs_12_26_9']])
else:
    st.warning("MACD/Signal Line not available (not enough data).")

# --- RSI Plot ---
st.subheader("📈 RSI Indicator")
if 'RSI' in data.columns:
    st.line_chart(data[['RSI']])
else:
    st.warning("RSI data not available.")
