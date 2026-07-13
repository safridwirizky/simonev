from pathlib import Path

class Config:
    SECRET_KEY = "simonev-secret-key"

    BASE_DIR = Path(__file__).resolve().parent

    EXCEL_FILE = BASE_DIR / "data" / "database.xlsx"

    CACHE_TIMEOUT = 300
