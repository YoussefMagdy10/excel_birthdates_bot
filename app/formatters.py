import calendar
from datetime import date

import pandas as pd


def _weekday_name_for_this_year(birthdate: pd.Timestamp, today: date) -> str:
    current_year_date = birthdate.date().replace(year=today.year)
    return calendar.day_name[current_year_date.weekday()]


def _format_contact_lines(row: pd.Series) -> list[str]:
    lines = []

    if row["boy_number"]:
        first_name = row["name"].split()[0] if row["name"] else "Student"
        lines.append(f"{first_name}: {row['boy_number']}")
    if row["mom_number"]:
        lines.append(f"Mother: {row['mom_number']}")
    if row["dad_number"]:
        lines.append(f"Father: {row['dad_number']}")

    return lines


def build_daily_email(rows: pd.DataFrame, today: date) -> tuple[str, str]:
    subject = f"Birthdays for {today.isoformat()}"
    body_lines = ["Today is the birthday of:", ""]

    for _, row in rows.iterrows():
        age = today.year - row["birthdate"].year
        body_lines.append(f"{row['name']}, now {age} years old!")
        body_lines.append("Wish them a happy birthday :)")
        body_lines.append("Contact phone numbers:")

        contacts = _format_contact_lines(row)
        if contacts:
            body_lines.extend(contacts)
        else:
            body_lines.append("No phone numbers available.")

        body_lines.append("")

    body = "\n".join(body_lines)
    return subject, body


def _build_period_section(title: str, rows: pd.DataFrame, today: date) -> str:
    lines = [title]

    if rows.empty:
        lines.append("-- Nobody --")
        return "\n".join(lines)

    for _, row in rows.iterrows():
        weekday = _weekday_name_for_this_year(row["birthdate"], today)
        display_date = row["birthdate"].strftime("%d-%m")
        lines.append(f"{weekday} {display_date} --> {row['name']}")

    return "\n".join(lines)


def build_weekly_email(
    last_week_rows: pd.DataFrame,
    next_week_rows: pd.DataFrame,
    today: date,
) -> tuple[str, str]:
    subject = f"Weekly birthdays - {today.isoformat()}"
    body = (
        _build_period_section("Last week was the birthday of:", last_week_rows, today)
        + "\n\n"
        + _build_period_section("This week is the birthday of:", next_week_rows, today)
    )
    return subject, body


def build_monthly_email(rows: pd.DataFrame, today: date) -> tuple[str, str]:
    subject = f"Birthdays for month {today.month}"
    body = _build_period_section("This month is the birthday of:", rows, today)
    return subject, body