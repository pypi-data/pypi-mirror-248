"""Provides tools to manipulate and format various time-based objects."""
import datetime
from dataclasses import dataclass
from onecondition import Validate


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
    """
    Validate.not_negative(seconds_in)

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
    """
    Validate.positive(day)

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
    """
    Validate.positive(day)

    return f"{day}{day_of_month_suffix(day)}"


def timezone_name(datetime_in: datetime.datetime) -> str:
    """Get the full timezone name from a datetime.datetime object.

    :param datetime.datetime datetime_in: The datetime.datetime object to get the timezone for.

    :return: A human-readable string with the full timezone name spelled out.
    :rtype: str
    """
    timezone = datetime_in.astimezone()

    return timezone.tzinfo.tzname(timezone)


class TimeString:
    """Data class with methods to format various datetime objects into human-readable strings."""
    @dataclass
    class TimeDelta:
        """Data class with methods to format datetime.timedelta objects and return human-readable strings."""
        @staticmethod
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

        @staticmethod
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

    @dataclass
    class DateTime:
        """Data class with methods to format datetime.datetime objects and return human-readable strings."""
        @staticmethod
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

        @staticmethod
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

    @staticmethod
    def automatic(
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
                return TimeString.DateTime.long(time_in)

            return TimeString.DateTime.short(time_in)

        if isinstance(time_in, datetime.timedelta):
            if long:
                return TimeString.TimeDelta.long(time_in)

            return TimeString.TimeDelta.short(time_in)

        raise TypeError(f"Time in must be either a datetime or timedelta object, not a {type(time_in)}")
