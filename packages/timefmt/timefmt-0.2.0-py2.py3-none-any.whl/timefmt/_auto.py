"""Provides a method to automatically convert a datetime or timedelta object to a human-readable string."""

import datetime

from timefmt import dt, td


def auto(
        time_in: datetime.datetime | datetime.timedelta,
        long: bool = False
):
    """Automatically convert a datetime.datetime or datetime.timedelta object to a string and return it.

    :param datetime.datetime | datetime.timedelta time_in: The object to convert.
    :param long: If we should return the long or short version.

    :raises TypeError: If the time_in is not a datetime.datetime or datetime.timedelta object

    :return: The input time in a human-readable format.
    :rtype: str
    """
    if isinstance(time_in, datetime.datetime):
        if long:
            return dt.long(time_in)

        return dt.short(time_in)

    if isinstance(time_in, datetime.timedelta):
        if long:
            return td.long(time_in)

        return td.short(time_in)

    raise TypeError(f"Time in must be either a datetime or timedelta object, not a {type(time_in)}")
