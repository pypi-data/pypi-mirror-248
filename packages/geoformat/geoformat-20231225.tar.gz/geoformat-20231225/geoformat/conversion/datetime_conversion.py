import datetime


def format_datetime_object_to_str_value(
    datetime_value, format=["year", "month", "day"]
):
    """
    Convert a datetime object to a string representation based on specified components.

    This function allows selective formatting of a datetime object into a string by choosing specific components
    such as year, month, day, hour, second, and microsecond. The components are concatenated in the order
    provided in the format list.

    Parameters:
    datetime_value (datetime): The datetime object to be formatted.
    format (list of str, optional): A list of string components to include in the output.
        Default is ["year", "month", "day"]. Valid components are "year", "month", "day", "hour",
        "second", and "microsecond".

    Returns:
    str: A string representation of the datetime object based on the specified format.

    Raises:
    Exception: If an invalid component is specified in the format list.
    """

    if isinstance(format, str):
        format = [format]

    return_value = ""
    for v in format:
        if v == "year":
            return_value += str(datetime_value.year).zfill(4)
        elif v == "month":
            return_value += str(datetime_value.month).zfill(2)
        elif v == "day":
            return_value += str(datetime_value.day).zfill(2)
        elif v == "hour":
            return_value += str(datetime_value.hour).zfill(2)
        elif v == "second":
            return_value += str(datetime_value.second).zfill(2)
        elif v == "microsecond":
            return_value += str(datetime_value.microsecond).zfill(6)
        else:
            raise Exception()

    return return_value


def date_to_int(date_value, epoch=datetime.date(1970, 1, 1)):
    """
    Convert a date object to an integer representing the number of days since a specified epoch.

    This function calculates the number of days from a given epoch (default is 1970-01-01) to the specified date.
    It's useful for converting date values into a consistent numeric format for calculations or storage.

    Parameters:
    date_value (datetime.date): The date value to be converted.
    epoch (datetime.date, optional): The epoch (start date) from which the days are counted.
        Default is 1970-01-01.

    Returns:
    int: The number of days from the epoch to the given date.
    """
    return (date_value - epoch).days


def time_to_int(time_value):
    """
    Convert a time object to an integer representing the time in microseconds.

    This function transforms a time object into an integer representing the total number of microseconds
    since midnight. It's useful for time calculations or storing time values in a compact numeric format.

    Parameters:
    time_value (datetime.time): The time value to be converted.

    Returns:
    int: The number of microseconds since midnight represented by the time object.
    """
    return int(
        time_value.hour * 3600 * 1e6
        + time_value.minute * 60 * 1e6
        + time_value.second * 1e6
        + time_value.microsecond
    )


def int_to_date(int_value, epoch=datetime.date(1970, 1, 1)):
    """
    Convert an integer representing the number of days since a specified epoch to a date object.

    Parameters:
    int_value (int): The number of days since the epoch.
    epoch (datetime.date, optional): The epoch (start date) from which the days are counted.
        Default is 1970-01-01.

    Returns:
    datetime.date: The date corresponding to the given number of days since the epoch.
    """
    return epoch + datetime.timedelta(days=int_value)


def int_to_time(int_value):
    """
    Convert an integer representing time in microseconds since midnight to a time object.

    Parameters:
    int_value (int): The number of microseconds since midnight.

    Returns:
    datetime.time: The time object represented by the given number of microseconds since midnight.
    """
    seconds, int_value = divmod(int_value, 1e6)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return datetime.time(int(hours), int(minutes), int(seconds), int(int_value))


def datetime_to_timestamp(datetime_value, epoch=datetime.datetime(1970, 1, 1)):
    """
    Converts a datetime object to a float representing the timestamp based on a specified epoch.

    This function calculates the number of seconds elapsed from a given epoch to the specified datetime value.
    It handles "naive" datetime objects (without timezone information) by assuming they are in the local timezone.
    It also aligns the epoch with the timezone of datetime_value before the calculation.

    Parameters:
    datetime_value (datetime.datetime): The datetime value to be converted.
    epoch (datetime.datetime, optional): The epoch (reference datetime) from which the time is counted.
        Defaults to January 1, 1970, 00:00:00.

    Returns:
    float: The timestamp (in seconds) from the epoch to the given datetime.

    Notes:
    - Naive datetime objects are treated as being in the local timezone.
    - The epoch is converted to the timezone of datetime_value for accurate calculation.
    """
    # If datetime_value is naive, assume it's in local time
    if (
        datetime_value.tzinfo is None
        or datetime_value.tzinfo.utcoffset(datetime_value) is None
    ):
        datetime_value = datetime_value.astimezone()

    # Convert epoch to the same timezone as datetime_value
    if epoch.tzinfo is None:
        epoch = epoch.replace(tzinfo=datetime.timezone.utc)

    # Calculate the difference in seconds
    delta = datetime_value - epoch
    timestamp = delta.total_seconds()

    return timestamp


def timestamp_to_datetime(timestamp, epoch=datetime.datetime(1970, 1, 1)):
    """
    Converts a timestamp (in seconds) to a datetime object based on a specified epoch.

    This function calculates the datetime value corresponding to a given number of seconds elapsed
    from a specified epoch. The function takes into account the timezone of the epoch.

    Parameters:
    timestamp (float): The number of seconds elapsed from the epoch.
    epoch (datetime.datetime, optional): The epoch (reference datetime) from which the time is counted.
        Defaults to January 1, 1970, 00:00:00.

    Returns:
    datetime.datetime: The datetime object corresponding to the given timestamp.

    Notes:
    - The resulting datetime object will be in the same timezone as the provided epoch.
    """
    # Ensure the epoch has timezone information
    if epoch.tzinfo is None:
        epoch = epoch.replace(tzinfo=datetime.timezone.utc)

    # Calculate the datetime corresponding to the timestamp
    return epoch + datetime.timedelta(seconds=timestamp)

