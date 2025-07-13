import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Investment Tracker", layout="wide")

st.title("📊 Investment Portfolio Dashboard")

# Load holdings from a CSV
uploaded_file = st.file_uploader("Upload your holdings CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Holdings")
    st.dataframe(df)

    tickers = df['Ticker'].tolist()
    prices = yf.download(tickers, period="1d", group_by='ticker', auto_adjust=True)

    def get_price(ticker):
        try:
            return prices[ticker]['Close'][-1]
        except:
            return None

    df['Current Price'] = df['Ticker'].apply(get_price)
    df['Market Value'] = df['Current Price'] * df['Quantity']
    df['Gain/Loss'] = df['Market Value'] - df['Quantity'] * df['Cost Basis']

    st.subheader("Performance")
    st.dataframe(df[['Ticker', 'Quantity', 'Cost Basis', 'Current Price', 'Market Value', 'Gain/Loss']])

    st.subheader("Sector Allocation")
    if 'Sector' in df.columns:
        fig = px.pie(df, names='Sector', values='Market Value', title='Sector Allocation')
        st.plotly_chart(fig)

    st.subheader("Total Portfolio Value")
    st.metric("Total Value", f"${df['Market Value'].sum():,.2f}")
else:
    st.info("Please upload a CSV file with columns: Ticker, Quantity, Cost Basis, Sector.")
