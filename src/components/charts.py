import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

def line_chart(df: pd.DataFrame, symbol: str, title: str):
    chart = alt.Chart(df).mark_line().encode(
        x='report_date:T',
        y='price:Q'
    ).properties(
        title=f'{title} for {symbol}',
        width='container'
    )
    st.altair_chart(chart, use_container_width=True)


def candle_stick_chart(df: pd.DataFrame, symbol: str):
    fig = go.Figure(data=[go.Candlestick(
        x=df['report_date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    # set y limits to be 10% above and below the min and max prices
    y_min = df['low'].min() * 0.9
    y_max = df['high'].max() * 1.1
    fig.update_yaxes(range=[y_min, y_max])
    fig.update_xaxes(
        type='date',
        tickformat='%Y-%m-%d',
        dtick='M1',  # Monthly ticks
        ticklabelmode='period'
    )

    fig.update_layout(
        title=f'Candlestick Chart for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    
    return fig