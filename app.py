"""Main Streamlit dashboard for MT5 Zone Monitor.

This application connects to a running MetaTrader 5 terminal, loads the visible
symbols, calculates daily and weekly support/resistance zones, and displays a
styled monitoring table. It also sends desktop notifications and audio alerts
when the current market price is near a defined zone.
"""

import pandas as pd
import streamlit as st
import time

import mt5_connector
import watchlist
import zone_calculator
import price_monitor
import alert_manager
import config

st.set_page_config(
    page_title="MT5 Zone Monitor",
    layout="wide"
)

st.title("MT5 Zone Monitor")


def highlight_zone_rows(df):
    """Apply row and cell highlighting for active zones."""

    zone_colors = {
        "Today High Zone": "background-color: #ffe6e6;",
        "Today Low Zone": "background-color: #e6ffe6;",
        "Yesterday High Zone": "background-color: #fff0cc;",
        "Yesterday Low Zone": "background-color: #e6f7ff;",
        "Current Week High Zone": "background-color: #ffd9b3;",
        "Current Week Low Zone": "background-color: #d9ffd9;",
        "Last Week High Zone": "background-color: #ffe0e6;",
        "Last Week Low Zone": "background-color: #e6f2ff;"
    }

    def style_row(row):
        if row["Status"] == "Safe":
            return [""] * len(row)

        active_zone = row["Status"].replace("Near ", "")
        styles = []

        for col in row.index:
            if col == active_zone:
                styles.append(zone_colors.get(active_zone, "background-color: #ffcccc;"))
            elif col in ("Symbol", "Status"):
                styles.append("background-color: #fff7cc;")
            else:
                styles.append("")

        return styles

    return df.style.apply(style_row, axis=1)


if "connected" not in st.session_state:
    mt5_connector.connect_mt5()
    st.session_state.connected = True

symbols = watchlist.get_watchlist_symbols()

if not symbols:
    st.error("No visible MT5 symbols were loaded. Please make sure MT5 is running and symbols are visible.")
    st.stop()

st.write("Symbols Loaded:", len(symbols))

if "alerts_sent" not in st.session_state:
    st.session_state.alerts_sent = {}

placeholder = st.empty()

while True:
    rows = []

    for symbol in symbols:
        price = price_monitor.get_symbol_price(symbol)
        if price is None:
            continue

        daily = zone_calculator.calculate_daily_levels(symbol)
        weekly = zone_calculator.calculate_weekly_levels(symbol)
        if daily is None:
            continue

        zones = {
            "Today High Zone": daily["today_high_zone"],
            "Today Low Zone": daily["today_low_zone"],
            "Yesterday High Zone": daily["yesterday_high_zone"],
            "Yesterday Low Zone": daily["yesterday_low_zone"]
        }

        if weekly:
            zones.update({
                "Current Week High Zone": weekly["cw_high_zone"],
                "Current Week Low Zone": weekly["cw_low_zone"],
                "Last Week High Zone": weekly["lw_high_zone"],
                "Last Week Low Zone": weekly["lw_low_zone"]
            })

        status = "Safe"

        for name, level in zones.items():
            if price_monitor.is_price_near_zone(symbol, price, level):
                status = f"Near {name}"
                alert_key = f"{symbol}:{name}"

                if alert_key not in st.session_state.alerts_sent:
                    alert_manager.send_alert(symbol, name)
                    st.session_state.alerts_sent[alert_key] = True

        rows.append({
            "Symbol": symbol,
            "Status": status,
            "Today High Zone": price_monitor.format_zone(symbol, daily["today_high_zone"], daily["today_high"]),
            "Today Low Zone": price_monitor.format_zone(symbol, daily["today_low"], daily["today_low_zone"]),
            "Yesterday High Zone": price_monitor.format_zone(symbol, daily["yesterday_high_zone"], daily["yesterday_high"]),
            "Yesterday Low Zone": price_monitor.format_zone(symbol, daily["yesterday_low"], daily["yesterday_low_zone"]),
            "Current Week High Zone": (price_monitor.format_zone(symbol, weekly["cw_high_zone"], weekly["cw_high"]) if weekly else None),
            "Current Week Low Zone": (price_monitor.format_zone(symbol, weekly["cw_low"], weekly["cw_low_zone"]) if weekly else None),
            "Last Week High Zone": (price_monitor.format_zone(symbol, weekly["lw_high_zone"], weekly["lw_high"]) if weekly else None),
            "Last Week Low Zone": (price_monitor.format_zone(symbol, weekly["lw_low"], weekly["lw_low_zone"]) if weekly else None)
        })

    df = pd.DataFrame(rows)
    styled = highlight_zone_rows(df)
    placeholder.dataframe(styled)

    time.sleep(config.CHECK_INTERVAL_SECONDS)
