import streamlit as st
from utils.database import load_detail_data, load_trend_data, get_stock_prices
from components.charts import *
import pandas as pd

st.set_page_config(page_title="Stock Analysis", layout="wide")
st.title("📊 Stock Analysis Dashboard")

@st.cache_data
def get_data():
    df = load_detail_data()
    trend = load_trend_data()
    return df, trend

df, trend = get_data()
symbols = sorted(df['symbol'].unique())
selected_symbol = st.selectbox("Select a Symbol", symbols)

@st.cache_data
def get_filtered_data(symbol):
    filtered_df = df[df['symbol'] == symbol]
    filtered_trend = trend[trend['symbol'] == symbol].copy()
    filtered_trend['report_date'] = filtered_trend['report_date'].astype(str).str[:10]
    price = get_stock_prices(symbol)
    if not price.empty:
        price['report_date'] = pd.to_datetime(price['report_date'], utc=False)
        price['report_date'] = price['report_date'].astype(str).str[:10]
        filtered_trend = filtered_trend.merge(price, on=['symbol', 'report_date'], how='left')
    return filtered_df, filtered_trend, price

filtered_df, filtered_trend, price = get_filtered_data(selected_symbol)

st.subheader(f"Details for {selected_symbol}")
st.dataframe(filtered_df, use_container_width=True)

st.subheader(f"Trend for {selected_symbol}")
st.dataframe(filtered_trend, use_container_width=True)

# line_chart(price, selected_symbol, "Latest Price")
price = price.rename(columns={
    'report_date': 'report_date',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'price': 'close'
})
chart = candle_stick_chart(price, selected_symbol)
st.plotly_chart(chart, use_container_width=True)