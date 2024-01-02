"""Provides methods to manipulate and format various time-based objects into human-readable strings."""

__version__ = "1.1.11"

__all__ = [
    "dt", "td",
    "SplitTime", "split_seconds", "day_of_month_suffix", "day_of_month_string", "timezone_name",
    "auto",
]

# TODO: Make timezone name universal across operating systems (may need tp literally make my own module, maybe pytz)

from timefmt._helpers import SplitTime, split_seconds, day_of_month_suffix, day_of_month_string, timezone_name
from timefmt._auto import auto
