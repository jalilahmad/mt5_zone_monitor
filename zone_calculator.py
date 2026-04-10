"""Zone calculation utilities for daily and weekly MT5 symbol ranges."""

import MetaTrader5 as mt5
import pandas as pd
from datetime import timedelta

import config
import time_utils


def get_rates(symbol, timeframe, bars):
    """Load price bars from MT5 and return a timezone-aware DataFrame."""

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None:
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    df['time'] = df['time'].dt.tz_convert(config.TIMEZONE)

    return df


def calculate_daily_levels(symbol):
    """Calculate daily high/low and target zone levels for the given symbol."""

    df = get_rates(symbol, mt5.TIMEFRAME_M1, 1440 * 5)
    if df is None or df.empty:
        return None

    now = time_utils.get_now()
    today_start = time_utils.get_day_start(now)
    yesterday_start = today_start - timedelta(days=1)

    today_df = df[df['time'] >= today_start]
    yesterday_df = df[(df['time'] >= yesterday_start) & (df['time'] < today_start)]

    if today_df.empty or yesterday_df.empty:
        return None

    today_high = today_df['high'].max()
    today_low = today_df['low'].min()
    yesterday_high = yesterday_df['high'].max()
    yesterday_low = yesterday_df['low'].min()

    today_range = today_high - today_low
    yesterday_range = yesterday_high - yesterday_low
    zone_percent = config.ZONE_PERCENT

    return {
        "today_high": today_high,
        "today_low": today_low,
        "yesterday_high": yesterday_high,
        "yesterday_low": yesterday_low,
        "today_high_zone": today_high - today_range * zone_percent,
        "today_low_zone": today_low + today_range * zone_percent,
        "yesterday_high_zone": yesterday_high - yesterday_range * zone_percent,
        "yesterday_low_zone": yesterday_low + yesterday_range * zone_percent
    }


def calculate_weekly_levels(symbol):
    """Calculate weekly high/low and zone levels for the given symbol."""

    df = get_rates(symbol, mt5.TIMEFRAME_M5, 12 * 24 * 14)
    if df is None or df.empty:
        return None

    now = time_utils.get_now()
    current_week_start = now - timedelta(days=now.weekday())
    last_week_start = current_week_start - timedelta(days=7)

    current_week_df = df[df['time'] >= current_week_start]
    last_week_df = df[(df['time'] >= last_week_start) & (df['time'] < current_week_start)]

    if current_week_df.empty or last_week_df.empty:
        return None

    cw_high = current_week_df['high'].max()
    cw_low = current_week_df['low'].min()
    lw_high = last_week_df['high'].max()
    lw_low = last_week_df['low'].min()

    cw_range = cw_high - cw_low
    lw_range = lw_high - lw_low
    zone_percent = config.ZONE_PERCENT

    return {
        "cw_high": cw_high,
        "cw_low": cw_low,
        "lw_high": lw_high,
        "lw_low": lw_low,
        "cw_high_zone": cw_high - cw_range * zone_percent,
        "cw_low_zone": cw_low + cw_range * zone_percent,
        "lw_high_zone": lw_high - lw_range * zone_percent,
        "lw_low_zone": lw_low + lw_range * zone_percent
    }
