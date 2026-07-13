from pathlib import Path


class Config:

    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"

    EXCEL_FILE = DATA_DIR / "database.xlsx"

    SETTINGS_FILE = DATA_DIR / "settings.json"
