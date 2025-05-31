import sqlite3
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# load environment variables
load_dotenv()
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:password@localhost:5432/market_data')
SCHEMA = os.getenv('DB_SCHEMA', 'public')

def load_detail_data():
    engine = create_engine(DB_URL)
    query = f'SELECT * FROM "{SCHEMA}"."screen5_detail"'
    df = pd.read_sql_query(query, engine)
    df = df[['report_date', 'symbol', 'latest_price', '52wk_high','ema_9',
             'ema_21', 'adx_14', 'rsi_14', '2_week_rpi', '3_month_rpi',
             '6_month_rpi', '2wk_sma_of_6m_rpi']].sort_values(by=['symbol', 'report_date'])
    return df

def load_trend_data():
    engine = create_engine(DB_URL)
    query = f'SELECT * FROM "{SCHEMA}"."screen5_trend"'
    trend = pd.read_sql_query(query, engine)
    trend = trend[['report_date', 'symbol', '52wk_high',
                   'trending_days', 'weighted_rpi', 'adx_14',
                   'rsi_14']].sort_values(by=['symbol', 'report_date'])    
    return trend


def get_stock_prices(symbol):
    engine = create_engine(DB_URL)
    query = text(f'SELECT * FROM "{SCHEMA}"."stock_prices" WHERE symbol = :symbol ORDER BY report_date')
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params={"symbol": symbol})
            # do not conver to  UTC
            df['report_date'] = pd.to_datetime(df['report_date'], utc=False)
        return df
    except IntegrityError as e:
        logging.error(f"Integrity error: {e}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error fetching stock prices for {symbol}: {e}")
        return pd.DataFrame()