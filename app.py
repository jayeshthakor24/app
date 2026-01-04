import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ---------- TITLE ----------
st.set_page_config(page_title="Stock Analysis App", layout="wide")
st.title("📈 Stock Market Analysis Software")

# ---------- INPUT ----------
stock_symbol = st.text_input("Enter Stock Symbol (NSE Example: TCS.NS, INFY.NS)", "TCS.NS")

def convert_market_cap(value):
    if value is None:
        return "NA"
    value = float(value)
    if value >= 1e7:
        return f"{value/1e7:.2f} Cr"
    elif value >= 1e5:
        return f"{value/1e5:.2f} Lakh"
    else:
        return f"{value:.2f} ₹"

# ---------- FETCH DATA ----------
if st.button("Fetch Data"):
    try:
        stock = yf.Ticker(stock_symbol)

        info = stock.info
        hist = stock.history(period="1y")

        # ---------- BASIC DETAILS ----------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧾 Basic Info")
            st.write(f"**Name:** {info.get('longName', 'NA')}")
            st.write(f"**Symbol:** {stock_symbol}")
            st.write(f"**Sector:** {info.get('sector', 'NA')}")

        with col2:
            st.subheader("💰 Market Cap")
            mc = convert_market_cap(info.get("marketCap"))
            st.write(f"**Market Cap:** {mc}")

        with col3:
            st.subheader("📊 Price Info")
            st.write(f"**Current Price:** {info.get('currentPrice', 'NA')} ₹")
            st.write(f"**52W High:** {info.get('fiftyTwoWeekHigh', 'NA')} ₹")
            st.write(f"**52W Low:** {info.get('fiftyTwoWeekLow', 'NA')} ₹")

        # ---------- TREND METER ----------
        st.subheader("📉 Trend Meter (Green / Red)")

        last_close = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2]

        if last_close > prev_close:
            st.success("📈 UP TREND (Green)")
        else:
            st.error("📉 DOWN TREND (Red)")

        # ---------- CANDLESTICK CHART ----------
        st.subheader("📊 Candlestick Chart (1 Year)")

        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])

        fig.update_layout(
            height=500,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("❌ Error fetching stock data — check symbol!")
        st.write(e)
