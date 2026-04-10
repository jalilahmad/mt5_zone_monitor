"""Application configuration for MT5 Zone Monitor."""

# =============================
# TIME SETTINGS
# =============================

# Timezone used for all MT5 time-based calculations.
TIMEZONE = "Asia/Kabul"

# Trading day start time in local timezone.
DAY_START_HOUR = 1
DAY_START_MINUTE = 30

# =============================
# ZONE SETTINGS
# =============================

# Zone width ratio used to calculate the alert range inside daily and weekly bars.
ZONE_PERCENT = 0.04   # 4% of the bar range

# How many pips away from a zone the price must be to trigger an alert.
ALERT_DISTANCE_PIPS = 3

# Delay between refresh cycles, in seconds.
CHECK_INTERVAL_SECONDS = 60

# =============================
# SOUND SETTINGS
# =============================

ALERT_SOUND_PATH = "assets/alert.wav"

# How long the alert sound should play, in seconds.
SOUND_DURATION_SECONDS = 10

# =============================
# MT5 SETTINGS
# =============================

# Optional local path to the MetaTrader 5 terminal installation.
MT5_PATH = None
