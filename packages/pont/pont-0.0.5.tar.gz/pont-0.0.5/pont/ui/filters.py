import datetime


def format_datetime(value: datetime.datetime):
    """
    Format a datetime object for display.

    Args:
        value datetime.datetime: The datetime object to format.
    """
    # If today, display only the time.
    if value.date() == datetime.date.today():
        return value.strftime("%H:%M:%S")
    return value.strftime("%Y-%m-%d %H:%M:%S")
