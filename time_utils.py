"""Timezone-aware date and time helpers for MT5 range calculations."""

from datetime import datetime, timedelta
import pytz

import config


def get_now():
    """Return the current datetime in the configured timezone."""

    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)


def get_day_start(now):
    """Return the start of the current trading day for a timezone-aware datetime."""

    start = now.replace(
        hour=config.DAY_START_HOUR,
        minute=config.DAY_START_MINUTE,
        second=0,
        microsecond=0
    )

    if now < start:
        start -= timedelta(days=1)

    return start


def get_yesterday_start(now):
    """Return the beginning of the previous trading day."""

    today_start = get_day_start(now)
    return today_start - timedelta(days=1)
