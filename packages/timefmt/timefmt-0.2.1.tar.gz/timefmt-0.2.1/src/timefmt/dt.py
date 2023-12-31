"""Contains methods to format datetime.datetime objects into human-readable strings."""
import datetime

from timefmt._helpers import day_of_month_string, timezone_name


def short(datetime_in: datetime.datetime) -> str:
    """Return the datetime.datetime object as a short human-readable string.

    :param datetime.datetime datetime_in: The timedelta to convert.

    :return: The datetime.datetime object as a short human-readable string
    :rtype: str
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
    """
    now = datetime.datetime.now()

    format_string = "%#I:%M:%S %p"

    if datetime_in.day != now.day or datetime_in.year != now.year:
        format_string = f"%A, %B {day_of_month_string(datetime_in.day)}, %Y at {format_string}"

    time_string = datetime_in.strftime(format_string).strip()
    time_string += f" {timezone_name(datetime_in)}"

    return time_string
