import sys

from app.runner import run_daily, run_monthly, run_weekly


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python scripts/run.py <daily|weekly|monthly> <institution_config_path>"
        )

    mode = sys.argv[1].strip().lower()
    config_path = sys.argv[2].strip()

    if mode == "daily":
        run_daily(config_path)
    elif mode == "weekly":
        run_weekly(config_path)
    elif mode == "monthly":
        run_monthly(config_path)
    else:
        raise SystemExit(f"Invalid mode '{mode}'. Use: daily, weekly, or monthly.")


if __name__ == "__main__":
    main()