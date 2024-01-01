"""Contains methods to format datetime.datetime objects into human-readable strings.

:Example:
    >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
    >>> short(test_datetime)
    '12:23:31 PM'
    >>> long(test_datetime)
    '12:23:31 PM MST'
"""
import datetime

from timefmt._helpers import day_of_month_string, timezone_name


def short(datetime_in: datetime.datetime) -> str:
    """Return the datetime.datetime object as a short human-readable string.

    :param datetime.datetime datetime_in: The timedelta to convert.

    :return: The datetime.datetime object as a short human-readable string
    :rtype: str

    :Example:
        >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
        >>> short(test_datetime)
        '12:23:31 PM'
        >>> test_datetime2 = datetime.datetime(2023, 12, 31, 12, 53, 10, 467258)
        >>> short(test_datetime2)
        '12:53:10 PM'
    """
    now = datetime.datetime.now()

    format_string = "%#I:%M:%S %p"

    if datetime_in.day != now.day or datetime_in.year != now.year:
        format_string = f"%Y/%m/%d @ {format_string}"

    return datetime_in.strftime(format_string).strip()


def long(datetime_in: datetime.datetime) -> str:
    """Return the datetime.datetime object as a long human-readable string.

    :param datetime.datetime datetime_in: The timedelta to convert.

    :return: The datetime.datetime object as a long human-readable string
    :rtype: str

    :Example:
        >>> test_datetime = datetime.datetime(2023, 12, 31, 12, 23, 31, 379292)
        >>> long(test_datetime)
        '12:23:31 PM MST'
        >>> test_datetime2 = datetime.datetime(2023, 12, 31, 12, 53, 10, 467258)
        >>> long(test_datetime2)
        '12:53:10 PM MST'
    """
    now = datetime.datetime.now()

    format_string = "%#I:%M:%S %p"

    if datetime_in.day != now.day or datetime_in.year != now.year:
        format_string = f"%A, %B {day_of_month_string(datetime_in.day)}, %Y at {format_string}"

    time_string = datetime_in.strftime(format_string).strip()
    time_string += f" {timezone_name(datetime_in)}"

    return time_string
