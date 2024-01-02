"""Provides a method to automatically convert a datetime or timedelta object to a human-readable string."""

import datetime
from onecondition import ValidationError

from timefmt import dt, td


def auto(
        time_in: datetime.datetime | datetime.timedelta,
        long: bool = False
):
    """Automatically convert a datetime.datetime or datetime.timedelta object to a string and return it.

    :param datetime.datetime | datetime.timedelta time_in: The object to convert.
    :param long: If we should return the long or short version.

    :raises onecondition.ValidationError: If the time_in is not a datetime.datetime or datetime.timedelta object

    :return: The input time in a human-readable format.
    :rtype: str

    :Example:
        >>> from freezegun import freeze_time
        >>> freezer = freeze_time("2023-12-31")
        >>> r = freezer.start()

        >>> from zoneinfo import ZoneInfo
        >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292, tzinfo=ZoneInfo("MST"))
        >>> auto(test_datetime)
        '12:23:31 PM'
        >>> auto(test_datetime, long=True)
        '12:23:31 PM MST'
        >>> test_timedelta = datetime.timedelta(hours=1000, seconds=9999)
        >>> auto(test_timedelta)
        '5W 6D 18:46:39'
        >>> auto(test_timedelta, long=True)
        '5 weeks, 6 days, 18 hours, 46 minutes, and 39 seconds'
        >>> auto(42)
        Traceback (most recent call last):
            ...
        onecondition.ValidationError: Value `42` must must be either a datetime or timedelta object, not a <class 'int'>
    """
    if isinstance(time_in, datetime.datetime):
        if long:
            return dt.long(time_in)

        return dt.short(time_in)

    if isinstance(time_in, datetime.timedelta):
        if long:
            return td.long(time_in)

        return td.short(time_in)

    raise ValidationError(time_in, f"must be either a datetime or timedelta object, not a {type(time_in)}")
