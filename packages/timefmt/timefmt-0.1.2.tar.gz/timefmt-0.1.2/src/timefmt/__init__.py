"""Provides methods to manipulate and format various time-based objects into human-readable strings."""

__version__ = "0.1.2"

from onecondition import ValidationError

from timefmt._helpers import SplitTime, split_seconds, day_of_month_suffix, day_of_month_string, timezone_name
from timefmt import dt, td
from timefmt._auto import auto
