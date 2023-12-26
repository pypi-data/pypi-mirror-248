import datetime

from . import _holiday


def now() -> datetime.datetime:
    """Return the current korean date and time."""

    tz = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.now(tz=tz)

    return dt


def is_weekend(dt: datetime.datetime) -> bool:
    """Return whether it is weekend or not."""

    week = dt.weekday()

    if week >= 5:
        return True
    else:
        return False


def is_holiday(dt: datetime.datetime) -> bool:
    """Return whether it is holiday or not."""

    year = dt.year
    date = dt.strftime('%Y-%m-%d')

    holiday = _holiday.holiday_from_file(year)
    if len(holiday) == 0:
        holiday = _holiday.holiday_from_krx(year)

    if date in holiday:
        return True
    else:
        return False


def is_closing_day(dt: datetime.datetime) -> bool:
    """Return whether it is a closing day or not."""

    if is_weekend(dt) or is_holiday(dt):
        return True
    else:
        return False


def is_trading_day(dt: datetime.datetime) -> bool:
    """Return whether it is a trading day or not."""

    return not is_closing_day(dt)


def trading_date(dt: datetime.datetime = None, base_time: int = 0) -> str:
    """Return trading date

    Return the previous date if it is the closing date or if it is before
    base_time. For example, the trading open time(ex. 09:00).
    """
    if dt is None:
        dt = now()

    # Before the base time
    if dt.hour < base_time:
        dt = dt - datetime.timedelta(days=1)

    while is_closing_day(dt):
        dt = dt - datetime.timedelta(days=1)

    date = dt.strftime('%Y%m%d')

    return date
