# MT5 Zone Monitor

MT5 Zone Monitor is a Streamlit dashboard that reads visible symbols from
MetaTrader 5 and calculates daily/weekly price zones for monitoring and alerts.
The app highlights active zones and sends desktop notifications when the current
price is close to a support/resistance zone.

## Features

- Connects to a running MetaTrader 5 terminal
- Loads visible symbols automatically
- Calculates daily and weekly zones based on high/low price bars
- Displays zone ranges in a Streamlit dashboard
- Highlights the active zone row and its column
- Sends desktop alerts with sound when price is near a zone
- Uses symbol decimal precision when formatting prices

## Prerequisites

- Python 3.11 or newer
- MetaTrader 5 installed and logged in
- An active Internet connection for package installation

## Installation

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows Command Prompt:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

### From the command line

```bash
streamlit run app.py
```

### From VS Code

1. Open the workspace folder in VS Code.
2. Open the Run and Debug panel.
3. Select `Run Streamlit App`.
4. Start the configuration.

This launches the Streamlit app in the integrated terminal and opens the local
app address in your browser.

## Configuration

The app configuration is stored in `config.py`:

- `TIMEZONE`: local timezone for MT5 chart data
- `DAY_START_HOUR` / `DAY_START_MINUTE`: local trading day start
- `ZONE_PERCENT`: percentage of the range used to build each alert zone
- `ALERT_DISTANCE_PIPS`: pip distance threshold for alerts
- `CHECK_INTERVAL_SECONDS`: refresh interval for the dashboard
- `ALERT_SOUND_PATH`: path to the alert sound file

## File Structure

- `app.py` - main Streamlit dashboard and alert loop
- `config.py` - application settings and constants
- `mt5_connector.py` - MetaTrader 5 connection helpers
- `watchlist.py` - loads visible symbols from MT5
- `zone_calculator.py` - calculates daily and weekly price zones
- `price_monitor.py` - symbol price formatting and distance checks
- `alert_manager.py` - desktop and sound notifications
- `time_utils.py` - timezone-aware datetime helpers
- `assets/` - media assets used by the application

## Notes

- Make sure MetaTrader 5 is running and the account is logged in before
  launching the app.
- The app uses the MT5 symbol decimal precision to format prices correctly.
- If no visible symbols are found, the dashboard shows an error message.

## GitHub Ready

This project includes:

- `requirements.txt` for dependency management
- `.vscode/launch.json` for running the Streamlit app from VS Code
- `.gitignore` to exclude generated files and local environment folders

## Troubleshooting

- `MT5 initialize failed`: verify MetaTrader 5 is installed and started.
- `Not logged in to MT5`: confirm the account is logged in inside MetaTrader 5.
- `No visible MT5 symbols were loaded`: ensure the symbol market watch list is visible.
