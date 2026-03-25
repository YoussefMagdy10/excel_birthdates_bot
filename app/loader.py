import json
import os
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["name", "birthdate", "boy_number", "mom_number", "dad_number"]

COLUMN_ALIASES = {
    "الإسم": "name",
    "الاسم": "name",
    "name": "name",
    "تاريخ الميلاد": "birthdate",
    "birthdate": "birthdate",
    "رقم الولد": "boy_number",
    "boy_number": "boy_number",
    "رقم الأم": "mom_number",
    "mom_number": "mom_number",
    "رقم الأب": "dad_number",
    "dad_number": "dad_number",
}


def load_institution_config(config_path: str) -> dict:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    required_keys = [
        "name",
        "sender_email",
        "sender_password_env",
        "subscribers",
        "csv_url",
    ]
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing config keys in {config_path}: {missing}")

    if not isinstance(config["subscribers"], list):
        raise ValueError("'subscribers' must be a list of email strings.")

    return config


def get_sender_password(env_var_name: str) -> str:
    password = os.environ.get(env_var_name)
    if not password:
        raise ValueError(
            f"Environment variable '{env_var_name}' is missing or empty."
        )
    return password


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {}
    for col in df.columns:
        normalized = COLUMN_ALIASES.get(col.strip())
        if normalized:
            renamed[col] = normalized

    df = df.rename(columns=renamed)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {missing}. "
            f"Supported aliases: {list(COLUMN_ALIASES.keys())}"
        )

    df = df[REQUIRED_COLUMNS].copy()
    return df


def load_students_dataframe(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    df = _normalize_columns(df)

    df["birthdate"] = pd.to_datetime(df["birthdate"], format="%d/%m/%Y", errors="coerce")
    if df["birthdate"].isna().any():
        bad_rows = df[df["birthdate"].isna()]
        raise ValueError(
            f"Some birthdate values could not be parsed with format DD/MM/YYYY.\n"
            f"Bad rows:\n{bad_rows.to_string(index=False)}"
        )

    for col in ["boy_number", "mom_number", "dad_number"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    df["name"] = df["name"].fillna("").astype(str).str.strip()

    return df