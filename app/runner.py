from datetime import datetime

import pandas as pd

from app.birthdays import (
    get_daily_birthdays,
    get_last_week_birthdays,
    get_month_birthdays,
    get_next_week_birthdays,
)
from app.formatters import (
    build_daily_email,
    build_monthly_email,
    build_weekly_email,
)
from app.loader import (
    get_sender_password,
    load_institution_config,
    load_students_dataframe,
)
from app.mailer import send_email


def _load_runtime(config_path: str) -> tuple[dict, pd.DataFrame, str]:
    config = load_institution_config(config_path)
    df = load_students_dataframe(config["csv_url"])
    sender_password = get_sender_password(config["sender_password_env"])
    return config, df, sender_password


def run_daily(config_path: str) -> None:
    today = datetime.now().date()
    config, df, sender_password = _load_runtime(config_path)

    rows = get_daily_birthdays(df, today)

    if rows.empty:
        print(f"[{config['name']}] No birthdays today.")
        return

    subject, body = build_daily_email(rows, today)

    print(f"[{config['name']}] Sending daily email...")
    print(body)

    send_email(
        subject=subject,
        body=body,
        sender_email=config["sender_email"],
        sender_password=sender_password,
        recipients=config["subscribers"],
    )
    print(f"[{config['name']}] Daily email sent successfully.")


def run_weekly(config_path: str) -> None:
    today = datetime.now().date()
    config, df, sender_password = _load_runtime(config_path)

    last_week_rows = get_last_week_birthdays(df, today)
    next_week_rows = get_next_week_birthdays(df, today)

    subject, body = build_weekly_email(last_week_rows, next_week_rows, today)

    print(f"[{config['name']}] Sending weekly email...")
    print(body)

    send_email(
        subject=subject,
        body=body,
        sender_email=config["sender_email"],
        sender_password=sender_password,
        recipients=config["subscribers"],
    )
    print(f"[{config['name']}] Weekly email sent successfully.")


def run_monthly(config_path: str) -> None:
    today = datetime.now().date()
    config, df, sender_password = _load_runtime(config_path)

    rows = get_month_birthdays(df, today)
    subject, body = build_monthly_email(rows, today)

    print(f"[{config['name']}] Sending monthly email...")
    print(body)

    send_email(
        subject=subject,
        body=body,
        sender_email=config["sender_email"],
        sender_password=sender_password,
        recipients=config["subscribers"],
    )
    print(f"[{config['name']}] Monthly email sent successfully.")