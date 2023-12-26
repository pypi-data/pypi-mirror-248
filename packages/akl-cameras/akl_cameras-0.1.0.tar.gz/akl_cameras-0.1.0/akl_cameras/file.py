from datetime import date
from pathlib import Path


def get_save_dir_path() -> Path:
    """Get a unique path to save images with each call."""

    current_date = date.today().strftime("%d-%m-%Y")
    current_day_dir = Path(f"photos/{current_date}")

    if not current_day_dir.exists():
        return Path.joinpath(current_day_dir, "0")

    elements_list = list(current_day_dir.iterdir())
    return Path.joinpath(current_day_dir, str(len(elements_list)))
