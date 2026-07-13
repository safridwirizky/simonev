from services.settings_service import SettingsService
from services.excel_service import ExcelService

settings_service = SettingsService(
    "data/settings.json"
)

excel_service = ExcelService()
