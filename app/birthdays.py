from datetime import date, timedelta

import pandas as pd


def sort_by_month_day(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    result = df.copy()
    result["month"] = result["birthdate"].dt.month
    result["day"] = result["birthdate"].dt.day
    result = result.sort_values(by=["month", "day", "name"], ascending=[True, True, True])
    return result.drop(columns=["month", "day"])


def get_daily_birthdays(df: pd.DataFrame, today: date) -> pd.DataFrame:
    rows = df[
        (df["birthdate"].dt.day == today.day) &
        (df["birthdate"].dt.month == today.month)
    ].copy()
    return sort_by_month_day(rows)


def _date_strings_between(start: date, end: date) -> list[str]:
    days = pd.date_range(start=start, end=end)
    return days.strftime("%d/%m").tolist()


def get_last_week_birthdays(df: pd.DataFrame, today: date) -> pd.DataFrame:
    start = today - timedelta(days=6)
    selected_days = _date_strings_between(start, today)

    rows = df[df["birthdate"].dt.strftime("%d/%m").isin(selected_days)].copy()
    return sort_by_month_day(rows)


def get_next_week_birthdays(df: pd.DataFrame, today: date) -> pd.DataFrame:
    end = today + timedelta(days=7)
    selected_days = _date_strings_between(today, end)

    rows = df[df["birthdate"].dt.strftime("%d/%m").isin(selected_days)].copy()
    return sort_by_month_day(rows)


def get_month_birthdays(df: pd.DataFrame, today: date) -> pd.DataFrame:
    rows = df[df["birthdate"].dt.month == today.month].copy()
    return sort_by_month_day(rows)