"""Provides methods to manipulate and format various time-based objects into human-readable strings.

:Example:
    >>> import timefmt
    >>> import datetime
    >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
    >>> test_timedelta = datetime.timedelta(hours=1000, seconds=9999)

    >>> timefmt.auto(test_datetime)
    '12:23:31 PM'
    >>> timefmt.auto(test_timedelta, long=True)
    '5 weeks, 6 days, 18 hours, 46 minutes, and 39 seconds'
"""

__version__ = "1.1.2"

from timefmt._helpers import SplitTime, split_seconds, day_of_month_suffix, day_of_month_string, timezone_name
from timefmt._auto import auto
