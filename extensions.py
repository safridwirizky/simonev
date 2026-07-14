from config import Config

from services.settings_service import SettingsService
from services.excel_service import ExcelService

settings_service = SettingsService(
    Config.SETTINGS_FILE
)

excel_service = ExcelService()
