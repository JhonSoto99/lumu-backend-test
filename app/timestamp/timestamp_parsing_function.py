from datetime import datetime, timezone
from typing import Optional, Union

MILLISECONDS_IN_ONE_SECOND: float = 1000.0
"""This constant represents the number of milliseconds in one second.
It is used to convert time values in milliseconds to their equivalent in seconds.
"""

SECONDS_THRESHOLD: int = 10_000_000_000
"""This threshold value (in seconds) is used to determine if a timestamp 
is in milliseconds or seconds. If a timestamp exceeds `SECONDS_THRESHOLD`,
it is assumed to be in milliseconds; otherwise, it is considered to be in seconds.
"""

LIST_DATES: list[Union[str, int, float]] = [
    "2021-12-03T16:15:30.235Z",
    "2021-12-03T16:15:30.235",
    "2021-10-28T00:00:00.000",
    "2011-12-03T10:15:30",
    1726668850124,
    "1726668850124",
    1726667942,
    "1726667942",
    969286895000,
    "969286895000",
    3336042095,
    "3336042095",
    3336042095000,
    "3336042095000",
]
""""A list of timestamps in various formats"""


def is_valid_timestamp(timestamp: Union[str, int]) -> bool:
    """Checks if a timestamp is valid. A timestamp is valid if:
    - It is a non-negative integer or float.
    - It is a string that can be converted to a float.

    Args:
        timestamp (Union[str, int]): The timestamp to validate.

    Returns:
        bool: True if the timestamp is valid, False otherwise.
    """
    if isinstance(timestamp, (int, float)):
        return timestamp >= 0

    if isinstance(timestamp, str):
        try:
            if timestamp.isdigit():
                float(timestamp)
            return True
        except ValueError:
            return False
    return False


def format_timestamp(timestamp: datetime) -> str:
    """Formats a datetime object into an ISO 8601 string with milliseconds and UTC timezone.

    Args:
        timestamp (datetime): The datetime object to format.

    Returns:
        str: The formatted timestamp in ISO 8601 format with 'Z' as the UTC indicator.
    """
    return timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def convert_unix_timestamp(timestamp: Union[int, float]) -> datetime:
    """Converts a UNIX timestamp to a datetime object in UTC.

    Args:
        timestamp (Union[int, float]): The UNIX timestamp to convert.

    Returns:
        datetime: The converted timestamp as a datetime object in UTC.
    """
    if timestamp > SECONDS_THRESHOLD:
        timestamp /= MILLISECONDS_IN_ONE_SECOND
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def analyze_timestamp(timestamp: Union[str, int]) -> Optional[str]:
    """Analyzes and converts a timestamp in various formats (int, float, or ISO string)
    to an ISO 8601 UTC datetime string with milliseconds precision.

    Args:
        timestamp (Union[str, int]): The timestamp to analyze, which can be:
            - An integer or float representing a UNIX timestamp in seconds or milliseconds.
            - A string representing a UNIX timestamp or ISO 8601 formatted date.

    Returns:
        Optional[str]: The converted timestamp in ISO 8601 format with 'Z' as the UTC indicator.

    Raises:
        ValueError: If the timestamp is invalid or an error occurs during conversion.
    """
    if not is_valid_timestamp(timestamp):
        raise ValueError(f"Invalid timestamp: {timestamp}")

    try:
        if isinstance(timestamp, (int, float)):
            timestamp = convert_unix_timestamp(float(timestamp))

        elif isinstance(timestamp, str):
            if timestamp.isdigit():
                timestamp = float(timestamp)
                timestamp = convert_unix_timestamp(float(timestamp))
            else:
                if timestamp.endswith("Z"):
                    timestamp = timestamp[:-1] + "+00:00"

                if "+" not in timestamp and "-" not in timestamp[-6:]:
                    timestamp += "+00:00"
                timestamp = datetime.fromisoformat(timestamp)
                timestamp = timestamp.astimezone(timezone.utc)

        return format_timestamp(timestamp)
    except ValueError as e:
        raise ValueError(f"Error converting timestamp '{timestamp}': {str(e)}") from e
    except Exception as e:
        raise ValueError(f"Unexpected error converting timestamp '{timestamp}': {str(e)}") from e


if __name__ == "__main__":
    for date in LIST_DATES:
        timestamp_utc = analyze_timestamp(date)
        print(f"{date} -> {timestamp_utc}")
