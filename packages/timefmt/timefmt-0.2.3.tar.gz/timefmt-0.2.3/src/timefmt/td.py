"""Contains methods to format datetime.timedelta objects into human-readable strings."""
import datetime

from timefmt._helpers import split_seconds


def short(timedelta_in: datetime.timedelta) -> str:
    """Return the datetime.timedelta object as a short human-readable string.

    :param datetime.timedelta timedelta_in: The timedelta to convert.

    :return: The datetime.timedelta object as a short human-readable string
    :rtype: str
    """
    ago_string = ""
    if timedelta_in < datetime.timedelta(0):
        timedelta_in = -timedelta_in
        ago_string += " ago"

    time_parts = split_seconds(timedelta_in.total_seconds())

    time_string = (f"{time_parts.hours}"
                   f":{time_parts.minutes:02}"
                   f":{time_parts.seconds:02}"
                   f"{ago_string}")

    if time_parts.days > 0:
        time_string = f"{time_parts.days}D {time_string}"

    if time_parts.weeks > 0:
        time_string = f"{time_parts.weeks}W {time_string}"

    return time_string


def long(timedelta_in: datetime.timedelta) -> str:
    """Return the datetime.timedelta object as a long human-readable string.

    :param datetime.timedelta timedelta_in: The timedelta to convert.

    :return: The datetime.timedelta object as a long human-readable string
    :rtype: str
    """
    ago_string = ""
    if timedelta_in < datetime.timedelta(0):
        timedelta_in = -timedelta_in
        ago_string += " ago"

    time_parts = split_seconds(timedelta_in.total_seconds())

    time_strings = []

    for value, name in (
            (time_parts.weeks, "week"),
            (time_parts.days, "day"),
            (time_parts.hours, "hour"),
            (time_parts.minutes, "minute"),
            (time_parts.seconds, "second")
    ):
        if name == "second":
            no_time_strings = len(time_strings) == 0
        else:
            no_time_strings = False

        if value > 0 or no_time_strings:
            time_strings.append(f"{value} {name}")
            if value != 1:
                time_strings[-1] += "s"

    if len(time_strings) == 1:
        time_string = f"{time_strings[0]}{ago_string}"
    elif len(time_strings) == 2:
        time_string = f"{time_strings[0]} and {time_strings[1]}{ago_string}"
    else:
        time_string = ", ".join(time_strings[:-1])
        time_string += f", and {time_strings[-1]}"
        time_string += ago_string

    return time_string
