"""Helper functions to aid with formatting time-based objects into human-readable text.

:Example:
    >>> split_seconds(123456789)
    SplitTime(weeks=204, days=0, hours=21, minutes=33, seconds=9, milliseconds=0)
    >>> day_of_month_suffix(23)
    'rd'
    >>> day_of_month_string(23)
    '23rd'
    >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
    >>> timezone_name(test_datetime)
    'MST'
"""
import datetime
from dataclasses import dataclass

import onecondition as oc
import onecondition.validate


@dataclass
class SplitTime:
    """Data class for holding split time values."""
    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int
    milliseconds: int | float


def split_seconds(seconds_in: int | float) -> SplitTime:
    """Split seconds into parts ranging from weeks to milliseconds and return a SplitTime object with those values.

    :param int seconds_in: The total number of seconds to split up.

    :raises ValidationError: Raised when a parameter is invalid.

    :return: A SplitTime object with the split weeks, days, hours, minutes, seconds, and milliseconds.
    :rtype: SplitTime

    :Example:
        >>> split_seconds(1.234)
        SplitTime(weeks=0, days=0, hours=0, minutes=0, seconds=1, milliseconds=234.0)
        >>> split_seconds(123456789)
        SplitTime(weeks=204, days=0, hours=21, minutes=33, seconds=9, milliseconds=0)
        >>> split_seconds(-3)
        Traceback (most recent call last):
            ...
        onecondition.ValidationError: Value `-3` must not be negative (non-zero)
    """
    oc.validate.not_negative(seconds_in)

    weeks, remainder = divmod(seconds_in, (60 ** 2) * 24 * 7)
    days, remainder = divmod(remainder, (60 ** 2) * 24)
    hours, remainder = divmod(remainder, 60 ** 2)
    minutes, remainder = divmod(remainder, 60)
    seconds = int(remainder)
    milliseconds = (remainder % 1) * 1000

    return SplitTime(
        weeks=int(weeks),
        days=int(days),
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=milliseconds
    )


def day_of_month_suffix(day: int) -> str:
    """Return the appropriate suffix for a specified day of the month.

    :param int day: The day of the month to get the suffix for.

    :raises ValidationError: Raised when a parameter is invalid.

    :return: A string that is either 'st', 'nd', 'rd', or 'th'.
    :rtype: str

    :Example:
        >>> day_of_month_suffix(1)
        'st'
        >>> day_of_month_suffix(23)
        'rd'
        >>> day_of_month_suffix(11)
        'th'
        >>> day_of_month_suffix(22)
        'nd'
        >>> day_of_month_suffix(26)
        'th'
    """
    oc.validate.positive(day)

    if day % 100 in [11, 12, 13]:
        return "th"

    match day % 10:
        case 1:
            return "st"
        case 2:
            return "nd"
        case 3:
            return "rd"
        case _:
            return "th"


def day_of_month_string(day: int) -> str:
    """Convert a numerical day of the month to a user-friendly string.

    :param int day: The day of the month to convert.

    :raises ValidationError: Raised when a parameter is invalid.

    :return: A string with the day of the month and an appropriate suffix ('st', 'nd', 'rd', or 'th').
    :rtype: str

    :Example:
        >>> day_of_month_string(1)
        '1st'
        >>> day_of_month_string(23)
        '23rd'
        >>> day_of_month_string(11)
        '11th'
        >>> day_of_month_string(22)
        '22nd'
        >>> day_of_month_string(26)
        '26th'
    """
    oc.validate.positive(day)

    return f"{day}{day_of_month_suffix(day)}"


def timezone_name(datetime_in: datetime.datetime) -> str:
    """Get the full timezone name from a datetime.datetime object.

    :param datetime.datetime datetime_in: The datetime.datetime object to get the timezone for.

    :return: A human-readable string with the timezone name (OS-specific formatting).
    :rtype: str

    :Example:
        >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
        >>> timezone_name(test_datetime)
        'MST'
    """
    timezone = datetime_in.astimezone()

    return timezone.tzinfo.tzname(timezone)
